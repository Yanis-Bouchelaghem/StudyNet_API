from django.db import models
from django.http.response import Http404
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
        department = self.request.query_params.get('department',None)
        if specialty:
            if Specialty.objects.filter(code=specialty).exists():
                return Section.objects.filter(specialty=specialty)
            else:
                raise Http404
        if department:
            if Department.objects.filter(code=department).exists():
                return Section.objects.filter(specialty__department__code=department)
            else:
                raise Http404
        return Section.objects.all()

    def get(self,request):
        sections = self.get_queryset()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

class SectionDetail(APIView):
    permission_classes = []

    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        teacher = self.get_object(pk)
        serializer = SectionSerializer(teacher)
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
    
    def get(self, request):
        section = self.request.query_params.get('section',None)
        if section:
            #Check that the section exists.
            if Section.objects.filter(code=section).exists():
                #Get the modules of this section.
                section_object = Section.objects.get(code=section)
                modules = section_object.modules.all()
                serializer = ModuleSerializer(modules,many=True,context={'section_code':section})
                return Response(serializer.data,status=status.HTTP_200_OK)
        #Section not given or does not exist.
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ModuleDetail(APIView):
    """
    Retrieves a specific module
    """
    permission_classes = []

    def get_object(self, pk):
        try:
            return Module.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        module = self.get_object(pk)
        serializer = ModuleSerializer(module)
        return Response(serializer.data)
