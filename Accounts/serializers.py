from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.db import transaction,IntegrityError

from Management.models import Module, Section,TeacherSection,Assignment,ModuleSection
from .models import User,Student,Teacher
from Management.serializers import SectionSerializer,AssignmentSerializer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect credentials.')

class CreateUserSerializer(serializers.ModelSerializer):
    """
        Used to display and create a user.
    """
    class Meta:
        model = User
        fields = ['id','password','email','first_name','last_name','date_joined']
        read_only_fields = ('date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    """
        Used to update a user.
    """
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ['email','first_name','last_name']

class StudentSerializer(serializers.ModelSerializer):
    """
        Only used to display a student with the details of their section.
    """
    user = CreateUserSerializer(many=False)
    section = SectionSerializer(many=False)
    class Meta:
        model = Student
        fields = '__all__'
        

class CreateStudentSerializer(serializers.ModelSerializer):
    """
        Used to display and create a student (The details of their section is not displayed, only the code).
    """
    user = CreateUserSerializer(many=False)
    class Meta:
        model = Student
        fields = '__all__'
    
    def validate(self, attrs):
        #Check that the group exists in the section.
        group = attrs['group']
        section = Section.objects.get(code=attrs['section'])
        if group < 1 or group > section.number_of_groups:
            raise serializers.ValidationError({'group':'This group does not exist in given section.'})
        return attrs
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        #Create the user
        user = User.objects.create_user(**user_data,user_type=User.Types.STUDENT)
        #Create the student account and assign to it the created user
        return Student.objects.create(**validated_data,user=user)

class TeacherSerializer(serializers.ModelSerializer):
    """
        Only used to display a teacher with his assignments.
    """
    user = CreateUserSerializer(many=False)
    assignments = AssignmentSerializer(many=True,required=False)
    
    class Meta:
        model = Teacher
        fields = '__all__'

class SimpleTeacherSerializer(serializers.ModelSerializer):
    """
        Only used to display a teacher without his assignments.
    """
    user = CreateUserSerializer(many=False)
    class Meta:
        model = Teacher
        exclude = ('sections',)

class SectionCharField(serializers.CharField):
    """
        An overriden serializer charfield with a custom validation.
        This charfield expects a section code then checks if that section exists.
    """
    def run_validation(self, data=serializers.empty):
        value = super().run_validation(data)
        #Check that the given section exists.
        if not Section.objects.filter(code=value).exists():
            raise ValidationError('section \"' + value + '\" does not exist.')
        return value

class CreateTeacherSerializer(serializers.ModelSerializer):
    """
        Only used to create a teacher with optionally their assigned sections.
    """
    user = CreateUserSerializer(many=False,required=True)
    sections = serializers.ListField(child=SectionCharField(),required=True)
    assignments = AssignmentSerializer(many=True,required=True)
    class Meta:
        model = Teacher
        fields = '__all__'

    def validate(self, attrs):
        sections = attrs['sections']
        assignements = attrs['assignments']
        department = attrs['department']
        #Check that the sections given in "sections" are part of the "department"
        for section in sections:
            #Get the section object
            section_object = Section.objects.get(code=section)
            if section_object.specialty.department.code != department.code:
                raise serializers.ValidationError({'sections':'One of the specified sections is not part of the department '+department.code})
        #Check that sections given in "assignments" are also given in "sections"
        for assignment in assignements:
            if not assignment['teacher_section']['section']['code'] in sections:
                raise serializers.ValidationError({'assignments':'Cannot assign a section not contained in this teacher\'s sections list.'})
        return attrs

    def create(self, validated_data):
        try:
            #Make sure to rollback if something goes wrong.
            with transaction.atomic():
                user_data = validated_data.pop('user')
                sections = validated_data.pop('sections',[])
                assignments = validated_data.pop('assignments',[])

                #Create the user.
                user = User.objects.create_user(**user_data,user_type=User.Types.TEACHER)
                #Create the teacher account and assign to it the created user.
                teacher = Teacher.objects.create(**validated_data,user=user)
                #Assign to the teacher the given sections.
                for section in sections:
                    section = Section.objects.get(code=section)
                    TeacherSection.objects.create(teacher=teacher,section=section)
                #Take care of the assignments
                for assignment in assignments:
                    section_code = assignment['teacher_section']['section']['code']
                    module_code = assignment['module_section']['module']['code']
                    teacher_section = TeacherSection.objects.get(teacher=teacher,section=section_code)
                    module_section = ModuleSection.objects.get(module=module_code,section=section_code)
                    Assignment.objects.create(teacher_section=teacher_section,
                    module_section=module_section,
                    module_type=assignment['module_type'],
                    concerned_groups=assignment['concerned_groups'])
                return teacher
        except IntegrityError:
            raise serializers.ValidationError({'assignments':'duplicate assignments.'})

class UpdateTeacherSerializer(serializers.ModelSerializer):
    """
        Only used to update a teacher.
        Requires a teacher id to be given in the context.
    """
    user = UpdateUserSerializer(many=False,required=True)
    sections = serializers.ListField(child=SectionCharField(),write_only=True)
    assignments = AssignmentSerializer(many=True,required=True)
    class Meta:
        model = Teacher
        fields = '__all__'

    def validate(self, attrs):
        sections = attrs['sections']
        assignements = attrs['assignments']
        department = attrs['department']

        #Check that the sections given in "sections" are part of the "department"
        for section in sections:
            #Get the section object
            section_object = Section.objects.get(code=section)
            if section_object.specialty.department.code != department.code:
                raise serializers.ValidationError({'sections':'One of the specified sections is not part of the department '+department.code})
        #Check that sections given in "assignments" are also given in "sections"
        for assignment in assignements:
            if not assignment['teacher_section']['section']['code'] in sections:
                raise serializers.ValidationError({'assignments':'Cannot assign a section not contained in this teacher\'s sections list.'})
        return attrs

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                teacher = instance
                user_data = validated_data.pop('user')
                sections = validated_data.pop('sections',[])
                assignments = validated_data.pop('assignments',[])
                #update the user data.
                instance.user.email = user_data.get('email',instance.user.email)
                instance.user.first_name = user_data.get('first_name',instance.user.first_name)
                instance.user.last_name = user_data.get('last_name',instance.user.last_name)
                instance.user.save()
                #update the teacher data.
                instance.grade = validated_data.get('grade',instance.grade)
                instance.department = validated_data.get('department',instance.department)
                instance.save()
                #update the TeacherSection relationships
                #start by deleting the removed sections
                old_teacher_section = TeacherSection.objects.filter(teacher=teacher)
                for teacher_section in old_teacher_section:
                    if not teacher_section.section.code in sections:
                        teacher_section.delete()
                #then add the new sections
                for section in sections:
                    if not TeacherSection.objects.filter(teacher=teacher,section=section).exists():
                        #relation with this section doesn't exist, create it.
                        section_object = Section.objects.get(code=section)
                        TeacherSection.objects.create(teacher=teacher,section=section_object)
                #update the teacher's assignments
                keep_assignments = []
                for assignment in assignments:
                    #Retrieve the necessarry relations
                    section = assignment['teacher_section']['section']['code']
                    module = assignment['module_section']['module']['code']
                    teacher_section = TeacherSection.objects.get(teacher=teacher,section=section)
                    module_section = ModuleSection.objects.get(module=module,section=section)
                    #Check if the given assignment contains an id
                    if 'id' in assignment.keys():
                        #Check if the given id exists in the database
                        if Assignment.objects.filter(id=assignment['id']).exists():
                            #Assignment exists, check that it concerns this teacher.
                            assignment_object = Assignment.objects.get(id=assignment['id'])
                            if assignment_object.teacher_section.teacher == teacher:
                                #update the assignment.
                                assignment_object.teacher_section = teacher_section
                                assignment_object.module_section = module_section
                                assignment_object.module_type = assignment['module_type']
                                assignment_object.concerned_groups = assignment['concerned_groups']
                                assignment_object.save()
                                keep_assignments.append(assignment_object.id)
                    else:
                        #Doesn't contain an id, create it.
                        new_assignment = Assignment.objects.create(teacher_section=teacher_section,
                        module_section=module_section,
                        module_type=assignment['module_type'],
                        concerned_groups=assignment['concerned_groups'])
                        keep_assignments.append(new_assignment.id)
                #Go through this teacher's assignments and remove
                #any ones that are missing from the request.
                for assignment in teacher.assignments:
                    if assignment.id in keep_assignments:
                        assignment.delete()
                #Done, return the teacher instance.
                return instance
        except IntegrityError:
            raise serializers.ValidationError({{'assignments':'duplicate assignments.'}})

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()