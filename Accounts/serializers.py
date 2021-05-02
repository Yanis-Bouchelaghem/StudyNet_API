from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate

from Management.models import Section,TeacherSection
from .models import User,Student,Teacher
from Management.serializers import SectionSerializer

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
        Only used to display a teacher.
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
    
    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        sections = validated_data.pop('sections',[])

        #Create the user.
        user = User.objects.create_user(**user_data,user_type=User.Types.TEACHER)
        #Create the teacher account and assign to it the created user.
        teacher = Teacher.objects.create(**validated_data,user=user)
        #Assign to the teacher the given sections.
        for section in sections:
            section = Section.objects.get(code=section)
            TeacherSection.objects.create(teacher=teacher,section=section)
        return teacher