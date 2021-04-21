from rest_framework import serializers
from .models import User,Student,Teacher

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','password','email','first_name','last_name','user_type','last_login','date_joined']
        read_only_fields = ('user_type','last_login','date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

class CreateStudentSerializer(serializers.ModelSerializer):
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


class CreateTeacherSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer(many=False)
    class Meta:
        model = Teacher
        fields = '__all__'
