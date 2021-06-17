from Accounts import serializers
from django.db.models.signals import pre_delete
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from fcm_django.fcm import fcm_send_topic_message
from fcm_django.models import FCMDevice

from .serializers import AppVersionSerializer, FCMTokenSerializer
from .models import AppVersionSupport
from Accounts.models import User
# Create your views here.

class AppVersionCheckView(APIView):
    """
        Checks if a certain app version is supported by this backend.
    """
    permission_classes = []

    def post(self, request):
        serializer = AppVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        version = serializer.validated_data['version']
        if AppVersionSupport.objects.filter(version=version).exists():
            version_object = AppVersionSupport.objects.get(version=version)
            if version_object.is_supported:
                #This version exists and is supported.
                return Response({'supported':True},status=status.HTTP_200_OK)
        #This version does not exist or is not supported.
        return Response({'supported':False},status=status.HTTP_400_BAD_REQUEST)

class TestFCM(APIView):

    permission_classes = []

    def post(self, request):
        fcm_send_topic_message(topic_name='ISIL-B-L3', message_body='Hello', message_title='A message')
        return Response()

class RegisterTeacherFCM(APIView):

    def post(self, request):
        if request.user.user_type == User.Types.TEACHER:
            serializer = FCMTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                #Check if his FCM token already exists
                existing = FCMDevice.objects.get(registration_id=serializer.data['FCM_token'])
                #It already exists, delete it
                existing.delete()
            except:
                #It doesn't exist, catch the exception and continue
                pass
            #Register the FCM token for this teacher
            FCMDevice.objects.create(registration_id=serializer.data['FCM_token'],user=request.user,type='android')
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({'invalid_user_type':'Only teachers can subscribe to individual notifications.'},
            status = status.HTTP_404_NOT_FOUND)

class UnregisterTeacherFCM(APIView):

     def post(self, request):
        if request.user.user_type == User.Types.TEACHER:
            serializer = FCMTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            #Delete the FCM token for this teacher
            try:
                fcm_device = FCMDevice.objects.get(registration_id=serializer.data['FCM_token'],user=request.user)
                fcm_device.delete()
                return Response(status = status.HTTP_200_OK)
            except FCMDevice.DoesNotExist:
                return Response(status = status.HTTP_404_NOT_FOUND)
        else:
            return Response({'invalid_user_type':'Only teachers can subscribe to individual notifications.'},
            status = status.HTTP_404_NOT_FOUND)
