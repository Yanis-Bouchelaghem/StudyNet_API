from rest_framework import serializers
from .models import User,Student,Teacher
from Management.models import Section,TeacherSection

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','password','email','first_name','last_name','user_type','last_login','date_joined']
        read_only_fields = ('user_type','last_login','date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

class CreateStudentSerializer(serializers.ModelSerializer):
    """

    """
    user = CreateUserSerializer(many=False)
    class Meta:
        model = Student
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        #Create the user
        user = User.objects.create_user(**user_data,user_type=User.Types.STUDENT)
        #Create the student account and assign to it the created user
        return Student.objects.create(**validated_data,user=user)


class TeacherSerializer(serializers.ModelSerializer):
    """
        Only used to display a teacher
    """
    user = CreateUserSerializer(many=False)
    class Meta:
        model = Teacher
        fields = '__all__'

class CreateTeacherSerializer(serializers.ModelSerializer):
    """
        Only used to create a teacher with their assigned sections
    """
    user = CreateUserSerializer(many=False)
    sections = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Teacher
        fields = '__all__'

    def validate(self, attrs):
        #Check that every given section exists.
        sections = attrs.get('sections',[])
        for section in sections:
            if not Section.objects.filter(code=section).exists():
                raise serializers.ValidationError({'sections':'section \"' + section + '\" does not exist.'})
        return attrs
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        sections = validated_data.pop('sections',[])

        #Create the user
        user = User.objects.create_user(**user_data,user_type=User.Types.TEACHER)
        #create the teacher
        teacher = Teacher.objects.create(**validated_data,user=user)
        #assign to him the given sections
        for section in sections:
            section = Section.objects.get(code=section)
            TeacherSection.objects.create(teacher=teacher,section=section)
        return teacher