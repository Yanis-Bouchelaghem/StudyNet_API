from rest_framework import serializers

from .models import AppVersionSupport

class AppVersionSerializer(serializers.Serializer):
    version = serializers.CharField(max_length=30)
    class Meta:
        fields = ['version',]