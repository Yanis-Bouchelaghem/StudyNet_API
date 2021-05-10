#View related imports
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken

#Custom imports
from .models import User,Student,Teacher
from Management.models import Section
from .serializers import (StudentSerializer,CreateUserSerializer, StudentSerializer, CreateStudentSerializer,
    TeacherSerializer, CreateTeacherSerializer, LoginSerializer, EmailSerializer, SimpleTeacherSerializer)

# Create your views here.
class StudentList(APIView):
    """
        Retrieves the list of students based on a section or create a student.
    """
    permission_classes=[]

    #Students can be filtered by section.
    def get_queryset(self):
        section = self.request.query_params.get('section',None)
        if section:
            return Student.objects.filter(section=section)
        return Student.objects.all()

    # Retrieves the list of students.
    def get(self,request):
        students = self.get_queryset()
        serializer = CreateStudentSerializer(students,many=True)
        return Response(serializer.data)

    # Creates a student.
    def post(self,request):
        serializer = CreateStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        #return the student data + a token to authenticate this student.
        student_data = StudentSerializer(student).data
        student_data["token"] = AuthToken.objects.create(user=student.user)[1]
        #Using StudentSerializer for the display to show the section detail.
        return Response(student_data, status=status.HTTP_201_CREATED)

class TeacherList(APIView):
    """
        Retrieves the list of teachers or create a teacher.
        Requires authentication.
    """
    def get_queryset(self):
        section = self.request.query_params.get('section',None)
        if section:
            if Section.objects.filter(code=section).exists():
                section_object = Section.objects.get(code=section)
                return section_object.teacher_set.all()
            else:
                #Section does not exist.
                return status.HTTP_404_NOT_FOUND
        return Teacher.objects.all()
    
    def get(self,request):
        teachers = self.get_queryset()
        if teachers != status.HTTP_404_NOT_FOUND:
            serializer = None
            if request.user.user_type == User.Types.ADMINISTRATOR:
                #If the user making the request is an admin, display the assignments.
                serializer = TeacherSerializer(teachers,many=True)
            else:
                #If the user making the request is not an admin, do not display the assignments.
                serializer = SimpleTeacherSerializer(teachers,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        #Given section doesn't exist.
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        #Check if the user that is creating the teacher is an admin.
        if request.user.user_type == User.Types.ADMINISTRATOR:
            serializer = CreateTeacherSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            teacher = serializer.save()
            #return the teacher data + a token to authenticate this teacher.
            return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Forbidden':'Only administrators may create teacher accounts.'},
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
        #Generate the user token.
        token = AuthToken.objects.create(user=user)[1]
        #Return the relevant information about the user + the authentication token.
        user_data = {}
        if user.user_type == User.Types.STUDENT:
            user_data = {'student': StudentSerializer(user.student).data}
            user_data['student']['token'] = token
        elif user.user_type == User.Types.TEACHER:
            user_data = {'teacher': TeacherSerializer(user.teacher).data}
            user_data['teacher']['token'] = token
        elif user.user_type == User.Types.ADMINISTRATOR:
            user_data = {'administrator': CreateUserSerializer(user).data}
            user_data['administrator']['token'] = token
        else:
            return Response({'Invalid_user_type':'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user_data,status=status.HTTP_201_CREATED)

class GetUserData(APIView):
    """
    Expects a token, returns the data of the user that owns the token.
    """

    def get(self, request):
        if request.user.user_type == User.Types.STUDENT:
            return Response({'student': StudentSerializer(request.user.student).data})
        elif request.user.user_type == User.Types.TEACHER:
            return Response({'teacher': TeacherSerializer(request.user.teacher).data})
        elif request.user.user_type == User.Types.ADMINISTRATOR:
            return Response({'administrator': CreateUserSerializer(request.user).data})
        else:
            return Response({'Invalid_user_type':'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)

class IsEmailAvailable(APIView):
    """
    Expects an email, returns whether or not this email is already taken or not
    """
    permission_classes = []

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({'email_taken':'This email is already taken.'},status=status.HTTP_302_FOUND)
        else:
            return Response({'email_available':'This email is available'},status=status.HTTP_200_OK)
