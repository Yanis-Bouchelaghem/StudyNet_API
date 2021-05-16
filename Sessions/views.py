from django.http.response import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView

from .models import Session
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
            serializer = SessionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'Unauthorized':'You can only update your own sessions.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Unauthorized':'Only teachers can update their sessions.'},status=status.HTTP_401_UNAUTHORIZED)