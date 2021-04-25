from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetup

class TestAppVersionCheck(TestSetup):
    """
    Unit tests for checking the support of a specific app version.
    """
    def test_supported_version(self):
        """
        Ensures that supported app versions are accepted.
        """
        url = reverse('app_version_check')
        response = self.client.post(url,{'version':'V0.3'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_unsupported_version(self):
        """
        Ensures that unsupported app versions are refused.
        """
        url = reverse('app_version_check')
        response = self.client.post(url,{'version':'V0.1'})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_nonexistent_version(self):
        """
        Ensures that versions that do not exist in the database are refused.
        """
        url = reverse('app_version_check')
        response = self.client.post(url,{'version':'V15.0'})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
