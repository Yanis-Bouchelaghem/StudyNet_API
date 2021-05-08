from rest_framework import serializers
from .models import Department,Specialty,Section,Assignment

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='teacher_section.section.code')
    class Meta:
        model = Assignment
        exclude = ('teacher_section',)