from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.db import transaction,IntegrityError

from Management.models import Section,TeacherSection,Assignment,ModuleSection
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
        fields = '__all__'

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
    sections = serializers.ListField(child=SectionCharField(),required=False)
    assignments = AssignmentSerializer(many=True,required=True)
    class Meta:
        model = Teacher
        fields = '__all__'

    def validate(self, attrs):
        #Check that sections given in "assignments" are also given in "sections"
        sections = attrs['sections']
        assignements = attrs['assignments']
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

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()