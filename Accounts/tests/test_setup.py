from rest_framework.test import APITestCase
from Management.models import Department,Specialty,Section
class TestSetup(APITestCase):

    def setUp(self):
        #Create mock department, specialty and sections
        self.department = Department.objects.create(code='CS',name='Computer science')
        self.specialty = Specialty.objects.create(Department=self.department,code='GD',name='Game design')
        self.section1 = Section.objects.create(code='GD A',specialty=self.specialty,number_of_groups=3)
        self.section2 = Section.objects.create(code='GD B',specialty=self.specialty,number_of_groups=4)
        #Mock student.
        self.student_data = {
            "user": {
                "email": "student1@me.com",
                "password": "userpass",
                "first_name": "user1",
                "last_name": "user1.1"
            },
            "registration_number": "181831068130",
            "group":1,
            "section": self.section1.code
        }

        #Mock teacher
        self.teacher_data = {
            "user": {
                "email": "teacher1@me.com",
                "password": "userpass",
                "first_name": "yanis",
                "last_name": "bouch"
            },
            "grade": "MAB",
            "sections": [
                self.section1.code,
                self.section2.code
            ]
        }
        return super().setUp()


    def tearDown(self):
        return super().tearDown()