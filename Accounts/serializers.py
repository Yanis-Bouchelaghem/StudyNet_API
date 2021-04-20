from rest_framework import serializers
from .models import User,Student

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