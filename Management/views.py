from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Department,Specialty,Section
from .serializers import DepartmentSerializer,SpecialtySerializer,SectionSerializer
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
            return Specialty.objects.filter(Department=department)
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
