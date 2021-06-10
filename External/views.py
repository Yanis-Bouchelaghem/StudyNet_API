from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from fcm_django.fcm import fcm_send_topic_message

from .serializers import AppVersionSerializer
from .models import AppVersionSupport
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