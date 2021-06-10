from django.http.response import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView

from Accounts.models import User
from .notifications import *
from utilities import ActionTypes
from .models import Homework,HomeworkHistory
from .serializers import HomeworkSerializer
# Create your views here.

class HomeworkList(APIView):
    """
    Retrieves the list of homeworks.
    Can be filtered by section.
    """

    def get_queryset(self):
        section = self.request.query_params.get('section',None)
        if section:
            return Homework.objects.filter(assignment__teacher_section__section__code=section)
        else:
            return Homework.objects.all()
    
    def get(self, request):
        homeworks = self.get_queryset()
        seriliazer = HomeworkSerializer(homeworks, many=True)
        return Response(seriliazer.data)

    def post(self, request):
        if request.user.user_type == User.Types.TEACHER:
            serializer = HomeworkSerializer(data=request.data, context={'teacher_id':request.user.id})
            serializer.is_valid(raise_exception=True)
            homework = serializer.save()
            #Add the creation of this homework to the history
            addToHomeworkHistory(homework,ActionTypes.ADD,request.user)
            #Send the notification to the students
            notifyHomeworkCreated(homework)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"Unauthorized":"Only teachers may create homeworks."},status=status.HTTP_401_UNAUTHORIZED)

class HomeworkDetail(APIView):

    def get_object(self, pk):
        try:
            return Homework.objects.get(pk=pk)
        except:
            raise Http404
    
    def get(self,request, pk):
        homework = self.get_object(pk)
        serializer = HomeworkSerializer(homework, context={'teacher_id':request.user.id})
        return Response(serializer.data)
    
    def put(self, request, pk):
        homework = self.get_object(pk)
        if request.user.user_type == User.Types.TEACHER:
            if homework.assignment.teacher_section.teacher.user.id == request.user.id:
                serializer = HomeworkSerializer(homework, data=request.data, context={'teacher_id':request.user.id})
                serializer.is_valid(raise_exception=True)
                homework = serializer.save()
                #Add the update of this homework to the history
                addToHomeworkHistory(homework,ActionTypes.UPDATE,request.user)
                #Send the notification to the students
                notifyHomeworkUpdated(homework)
                return Response(serializer.data)
            else:
                return Response({'Unauthorized':'You can only update your own homeworks.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Unauthorized':'Only teachers can update their homeworks.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk):
        homework = self.get_object(pk)
        #Check that this user is a teacher
        if request.user.user_type == User.Types.TEACHER:
            #Check that this homework has been created by this teacher
            if homework.assignment.teacher_section.teacher.user.id == request.user.id:
                homework.delete()
                #Add the deletion of this homework to the history
                addToHomeworkHistory(homework,ActionTypes.DELETE,request.user)
                #Send the notification to the students
                notifyHomeworkDeleted(homework)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Unauthorized':'You can only delete your own homeworks.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Unauthorized':'Only teachers can delete their homeworks.'}, status=status.HTTP_401_UNAUTHORIZED)

def addToHomeworkHistory(homework, action_type, user):
    HomeworkHistory.objects.create(
                    teacher=homework.assignment.teacher_section.teacher,
                    section=homework.assignment.teacher_section.section,
                    module=homework.assignment.module_section.module,
                    module_type=homework.assignment.module_type,
                    concerned_groups=homework.concerned_groups,
                    title=homework.title,
                    due_date=homework.due_date,
                    due_time=homework.due_time,
                    comment=homework.comment,
                    action_type=action_type,
                    author=user
                )