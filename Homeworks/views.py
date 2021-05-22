from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView

from Accounts.models import User
from .models import Homework
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
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"Unauthorized":"Only teachers may create homeworks."},status=status.HTTP_401_UNAUTHORIZED)