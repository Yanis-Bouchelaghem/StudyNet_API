#View related imports
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
#Custom imports
from .models import Student
from .serializers import CreateStudentSerializer

# Create your views here.
class StudentList(APIView):
    #TODO : Require authentication when done with login view (uncomment below).
    #permission_classes=[IsAuthenticated]
    def get(self,request):
        students = Student.objects.all()
        serializer = CreateStudentSerializer(students,many=True)
        return Response(serializer.data)