from rest_framework import serializers

from .models import AppVersionSupport
class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersionSupport
        fields = ['version',]