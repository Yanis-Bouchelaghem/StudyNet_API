from rest_framework.test import APITestCase
from External.models import AppVersionSupport
class TestSetup(APITestCase):

    def setUp(self):
        #Create supported and unsupported versions
        AppVersionSupport.objects.create(version='V0.1',is_supported=False)
        AppVersionSupport.objects.create(version='V0.2',is_supported=False)
        AppVersionSupport.objects.create(version='V0.3',is_supported=True)
        AppVersionSupport.objects.create(version='V0.4',is_supported=True)
        return super().setUp()