#View related imports
from django.http.response import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken

#Custom imports
from .models import User,Student,Teacher
from Management.models import Section
from .serializers import *

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
        department = self.request.query_params.get('department',None)
        if section:
            try:
                section_object = Section.objects.get(code=section)
                return section_object.teacher_set.all()
            except:
                raise Http404
        if department:
            return Teacher.objects.filter(department=department)
        
        #no section or department specified
        return status.HTTP_404_NOT_FOUND
    
    def get(self,request):
        teachers = self.get_queryset()
        if teachers != status.HTTP_404_NOT_FOUND:
            serializer = TeacherSerializer(teachers,many=True)
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

class TeacherDetail(APIView):
    """
        Retrieves the list of students based on a section or create a student.
    """

    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk):
        #Check if the user that is updating the teacher is an admin.
        if request.user.user_type == User.Types.ADMINISTRATOR:
            teacher = self.get_object(pk)
            serializer = UpdateTeacherSerializer(teacher, data=request.data,context={'teacher_id':pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

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
