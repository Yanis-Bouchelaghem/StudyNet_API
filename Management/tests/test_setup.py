from rest_framework.test import APITestCase

from Management.models import Department,Specialty,Section
class TestSetup(APITestCase):
    
    def setUp(self):
        #Create dummy department, specialty and sections
        self.department = Department.objects.create(code='CS',name='Computer science')
        self.specialty = Specialty.objects.create(department=self.department,code='GD',name='Game design')
        self.section1 = Section.objects.create(code='GD A',specialty=self.specialty,number_of_groups=3)
        self.section2 = Section.objects.create(code='GD B',specialty=self.specialty,number_of_groups=4)
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()