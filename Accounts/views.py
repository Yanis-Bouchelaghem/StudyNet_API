#View related imports
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken

#Custom imports
from .models import User,Student,Teacher
from .serializers import (CreateUserSerializer,CreateStudentSerializer,TeacherSerializer,
    CreateTeacherSerializer,LoginSerializer)

# Create your views here.
class StudentList(APIView):
    """
        Retrieves the list of students or create a student.
    """
    permission_classes=[]

    # Retrieves the list of students.
    def get(self,request):
        students = Student.objects.all()
        serializer = CreateStudentSerializer(students,many=True)
        return Response(serializer.data)
    
    # Creates a student.
    def post(self,request):
        serializer = CreateStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        #return the student data + a token to authenticate this student.
        return Response(
            {
            "student" : serializer.data,
            "token": AuthToken.objects.create(user=student.user)[1]
            },
            status=status.HTTP_201_CREATED)

class TeacherList(APIView):
    """
        Retrieves the list of teachers or create a teacher.
        Requires authentication.
    """
    def get(self,request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers,many=True)
        return Response(serializer.data)

    def post(self,request):
        #Check if the user that is creating the teacher is an admin.
        if request.user.user_type == User.Types.ADMINISTRATOR:
            serializer = CreateTeacherSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            teacher = serializer.save()
            #return the teacher data + a token to authenticate this teacher.
            return Response(
                {
                "teacher" : TeacherSerializer(teacher).data
                },
                status=status.HTTP_201_CREATED)
        else:
            return Response({'Forbidden':'Only administators may create teacher accounts.'},
                status=status.HTTP_403_FORBIDDEN)

class Login(APIView):
    """
        Requires email and password, returns the relevant user data + an authentication token.
    """
    permission_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        #Return the relevant information about the user.
        user_data = {}
        if user.user_type == User.Types.STUDENT:
            user_data = {'student': CreateStudentSerializer(user.student).data}
        elif user.user_type == User.Types.TEACHER:
            user_data = {'teacher': TeacherSerializer(user.teacher).data}
        elif user.user_type == User.Types.ADMINISTRATOR:
            user_data = {'administrator': CreateUserSerializer(user).data}
        else:
            return Response({'Invalid_user_type':'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_data['token'] = AuthToken.objects.create(user=user)[1]
        return Response(user_data,status=status.HTTP_201_CREATED)