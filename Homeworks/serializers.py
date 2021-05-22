from rest_framework import serializers
from .models import Homework

class HomeworkSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    teacher_email = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    module_type = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
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
    def get_section(self, instance):
        return instance.assignment.module_section.section.code

    def validate(self, attrs):
        #A teacher should only be able to create a homework using one of his assignments, not the assignment of another teacher.
        if attrs['assignment'].teacher_section.teacher.user.id != self.context['teacher_id']:
            raise serializers.ValidationError({'assignment':'This assignment does not concern you.'})
        #Check that all of the concerned groups exist in the assignment
        concerned_groups = attrs['concerned_groups']
        assignment_concerned_groups = attrs['assignment'].concerned_groups
        for group in concerned_groups:
            if not group in assignment_concerned_groups:
                raise serializers.ValidationError({'concerned_groups':'One of the specified groups does not exist in assignment.'})
        return attrs