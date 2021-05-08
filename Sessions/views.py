from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Session
from .serializers import SessionSerializer
# Create your views here.

class SessionList(APIView):
    """
    Retrieves the list of sessions
    """
    #TODO: Remove empty permission classes when done developing.
    permission_classes = []

    def get(self,request):
        sessions = Session.objects.all()
        seriliazer = SessionSerializer(sessions, many=True)
        return Response(seriliazer.data)