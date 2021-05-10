from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    teacher_email = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    module_type = serializers.SerializerMethodField()

    read_only_fields = ('teacher_name','teacher_email','module','module_type')
    class Meta:
        model = Session
        fields = '__all__'
    
    def get_teacher_name(self, instance):
        return instance.assignment.teacher_section.teacher.user.last_name[0]+'. '+ instance.assignment.teacher_section.teacher.user.first_name
    def get_teacher_email(self, instance):
        return instance.assignment.teacher_section.teacher.user.email
    def get_module(self, instance):
        return instance.assignment.module_section.module.name
    def get_module_type(self, instance):
        return instance.assignment.module_type
    
    def validate(self, attrs):
        #Check that the end time is after the start time
        if attrs['start_time'] > attrs['end_time']:
            raise serializers.ValidationError({'end_time':'The end time must be after the start time.'})
        #Check that all of the concerned groups exist in the assignment
        concerned_groups = attrs['concerned_groups']
        assignment_concerned_groups = attrs['assignment'].concerned_groups
        for group in concerned_groups:
            if not group in assignment_concerned_groups:
                raise serializers.ValidationError({'concerned_groups':'One of the specified groups does not exist in assignment.'})
        return attrs