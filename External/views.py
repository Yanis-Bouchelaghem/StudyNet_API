from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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
                return Response({'supported':'Version ' + version + ' is supported.'},status=status.HTTP_200_OK)
        #This version does not exist or is not supported.
        return Response({'not_supported':'Version ' + version + ' is not supported.'},status=status.HTTP_400_BAD_REQUEST)