from django.http.response import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
import copy

from utilities import ActionTypes
from .models import Session,SessionHistory
from .notifications import *
from .serializers import SessionSerializer
from Accounts.models import User
# Create your views here.

class SessionList(APIView):
    """
    Retrieves the list of sessions.
    Can be filtered by section.
    """

    def get_queryset(self):
        section = self.request.query_params.get('section',None)
        if section:
            return Session.objects.filter(assignment__teacher_section__section__code=section)
        else:
            return Session.objects.all()
    
    def get(self,request):
        sessions = self.get_queryset()
        seriliazer = SessionSerializer(sessions, many=True)
        return Response(seriliazer.data)
    
    def post(self, request):
        if request.user.user_type == User.Types.TEACHER:
            serializer = SessionSerializer(data=request.data, context={'teacher_id':request.user.id})
            serializer.is_valid(raise_exception=True)
            session = serializer.save()
            #Add the creation of this session to the history
            addToSessionHistory(session,ActionTypes.ADD,request.user)
            #Send the notification to the students
            notifySessionCreated(session)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"Unauthorized":"Only teachers may create sessions."},status=status.HTTP_401_UNAUTHORIZED)

class SessionDetail(APIView):

    def get_object(self, pk):
        try:
            return Session.objects.get(pk=pk)
        except:
            raise Http404
    
    def get(self,request, pk):
        session = self.get_object(pk)
        serializer = SessionSerializer(session, context={'teacher_id':request.user.id})
        return Response(serializer.data)
    
    def put(self, request, pk):
        session = self.get_object(pk)
        if request.user.user_type == User.Types.TEACHER:
            if session.assignment.teacher_section.teacher.user.id == request.user.id:
                serializer = SessionSerializer(session, data=request.data, context={'id':pk,'teacher_id':request.user.id})
                serializer.is_valid(raise_exception=True)
                #make a copy of the old session data
                old_session = copy.deepcopy(session)
                serializer.save()
                #Add the update of this session to the history
                addToSessionHistory(session,ActionTypes.UPDATE,request.user)
                #Send the notification to the students
                notifySessionUpdated(old_session,session)
                return Response(serializer.data)
            else:
                return Response({'Unauthorized':'You can only update your own sessions.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Unauthorized':'Only teachers can update their sessions.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk):
        session = self.get_object(pk)
        #Check that this user is a teacher
        if request.user.user_type == User.Types.TEACHER:
            #Check that this session has been created by this teacher
            if session.assignment.teacher_section.teacher.user.id == request.user.id:
                session.delete()
                #Add the deletion of this session to the history
                addToSessionHistory(session,ActionTypes.DELETE,request.user)
                #Send the notification to the students
                notifySessionDeleted(session)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Unauthorized':'You can only delete your own sessions.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Unauthorized':'Only teachers can delete their sessions.'}, status=status.HTTP_401_UNAUTHORIZED)

#Creates an entry in the session history table using the given data.
def addToSessionHistory(session, action_type, user):
    SessionHistory.objects.create(
                    teacher=session.assignment.teacher_section.teacher,
                    section=session.assignment.teacher_section.section,
                    module=session.assignment.module_section.module,
                    module_type=session.assignment.module_type,
                    concerned_groups=session.concerned_groups,
                    day=session.day,
                    start_time=session.start_time,
                    end_time=session.end_time,
                    meeting_link=session.meeting_link,
                    meeting_password=session.meeting_password,
                    comment=session.comment,
                    action_type=action_type,
                    author=user
                )