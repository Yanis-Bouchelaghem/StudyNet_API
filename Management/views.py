from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Department,Specialty,Section,Assignment,Module
from .serializers import (DepartmentSerializer,SpecialtySerializer,
SectionSerializer,AssignmentSerializer,ModuleSerializer)
# Create your views here.

class DepartmentList(APIView):
    """
        Retrieves the list of departments.
    """
    permission_classes = []

    def get(self,request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class SpecialtyList(APIView):
    """
        Retrieves the list of specialties.
        Can be filtered by department.
    """
    permission_classes = []

    def get_queryset(self):
        department = self.request.query_params.get('department',None)
        if department:
            return Specialty.objects.filter(department=department)
        return Specialty.objects.all()
    
    def get(self,request):
        specialties = self.get_queryset()
        serializer = SpecialtySerializer(specialties, many=True)
        return Response(serializer.data)

class SectionList(APIView):
    """
        Retrieves the list of sections.
        Can be filtered by specialty.
    """
    permission_classes = []

    def get_queryset(self):
        specialty = self.request.query_params.get('specialty',None)
        if specialty:
            return Section.objects.filter(specialty=specialty)
        return Section.objects.all()

    def get(self,request):
        sections = self.get_queryset()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

class AssignmentList(APIView):
    """
    Retrieves the list of assignments
    """
    #TODO : Think about permission classes after finishing development.
    permission_classes = []

    def get(self,request):
        assignements = Assignment.objects.all()
        serializer = AssignmentSerializer(assignements,many=True)
        return Response(serializer.data)

class ModuleList(APIView):
    """
    Retrieves the list of modules based on a section.
    """
    permission_classes = []

    def get_queryset(self):
        section = self.request.query_params.get('section',None)
        if section:
            #Check that the section exists
            if Section.objects.filter(code=section).exists():
                #Get the modules of this section
                section_object = Section.objects.get(code=section)
                return section_object.modules.all()
            else:
                return status.HTTP_404_NOT_FOUND
        #If no section is given, return all modules.
        return Module.objects.all()
    
    def get(self, request):
        modules = self.get_queryset()
        #Check if the section has been found.
        if modules != status.HTTP_404_NOT_FOUND:
            serializer = ModuleSerializer(modules,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)