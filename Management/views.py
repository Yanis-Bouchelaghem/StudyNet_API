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
    """
    permission_classes = []

    def get(self,request):
        specialties = Specialty.objects.all()
        serializer = SpecialtySerializer(specialties, many=True)
        return Response(serializer.data)

class SectionList(APIView):
    """
        Retrieves the list of sections.
    """
    permission_classes = []

    def get(self,request):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)