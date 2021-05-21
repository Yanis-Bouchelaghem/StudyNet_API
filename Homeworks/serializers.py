from rest_framework import serializers
from .models import Homework

class HomeworkSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    teacher_email = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    module_type = serializers.SerializerMethodField()
    class Meta:
        model = Homework
        fields = '__all__'

    def get_teacher_name(self, instance):
        return instance.assignment.teacher_section.teacher.user.last_name+' '+ instance.assignment.teacher_section.teacher.user.first_name[0] + '.'
    def get_teacher_email(self, instance):
        return instance.assignment.teacher_section.teacher.user.email
    def get_module(self, instance):
        return instance.assignment.module_section.module.code
    def get_module_type(self, instance):
        return instance.assignment.module_type