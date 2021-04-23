from rest_framework.test import APITestCase
from knox.models import AuthToken
from Management.models import Department,Specialty,Section
from Accounts.models import User,Teacher,Student
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
                "first_name": "teacher1",
                "last_name": "teacher1"
            },
            "grade": "MAB",
            "sections": [
                self.section1.code,
                self.section2.code
            ]
        }
        #Create an admin user and a token.
        self.admin_user = User.objects.create_user(email='admin@me.com',first_name='admin',last_name='admin',
        password='adminpass',user_type=User.Types.ADMINISTRATOR)
        self.admin_user_token = AuthToken.objects.create(user=self.admin_user)
        
        #Create a teacher user, their account and a token.
        self.teacher_user = User.objects.create_user(email='teacher@me.com',first_name='teacher',last_name='teacher',
        password='teacherpass',user_type=User.Types.TEACHER)
        self.teacher_user_token = AuthToken.objects.create(user=self.teacher_user)
        self.teacher_account = Teacher.objects.create(user=self.teacher_user,grade='MAB')
        
        #Create a student user, their account and a token.
        self.student_user = User.objects.create_user(email='student@me.com',first_name='student',last_name='student',
        password='studentpass',user_type=User.Types.STUDENT)
        self.student_user_token = AuthToken.objects.create(user=self.student_user)
        self.student_account = Student.objects.create(user=self.student_user,section=self.section1,
        registration_number='151638468951',group=1)

        #Create a superuser and a token.
        self.super_user = User.objects.create_superuser(email='superuser@me.com',first_name='superuser',last_name='superuser',
        password='superuserpass')
        self.super_user_token = AuthToken.objects.create(user=self.super_user)
        return super().setUp()

        


    def tearDown(self):
        return super().tearDown()