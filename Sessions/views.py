from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Session
from .serializers import SessionSerializer
# Create your views here.

class SessionList(APIView):
    """
    Retrieves the list of sessions.
    Can be filtered by section.
    """
    #TODO: Remove empty permission classes when done developing.
    permission_classes = []

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