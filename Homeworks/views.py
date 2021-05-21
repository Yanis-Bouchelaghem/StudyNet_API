from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView

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
    
    def get(self,request):
        homeworks = self.get_queryset()
        seriliazer = HomeworkSerializer(homeworks, many=True)
        return Response(seriliazer.data)