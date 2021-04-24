from rest_framework.test import APITestCase
from knox.models import AuthToken
from Management.models import Department,Specialty,Section
from Accounts.models import User,Teacher,Student
class TestSetup(APITestCase):

    def setUp(self):
        #Create dummy department, specialty and sections
        self.department = Department.objects.create(code='CS',name='Computer science')
        self.specialty = Specialty.objects.create(Department=self.department,code='GD',name='Game design')
        self.section1 = Section.objects.create(code='GD A',specialty=self.specialty,number_of_groups=3)
        self.section2 = Section.objects.create(code='GD B',specialty=self.specialty,number_of_groups=4)
        #Dummy student data.
        self.valid_student_data = {
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

        #Dock teacher data.
        self.valid_teacher_data = {
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
        return super().setUp()

    def create_dummy_admin(self):
        """
        returns a dictionary containing the admin user data and the token.
        """
        admin_user = User.objects.create_user(email='admin@me.com',first_name='admin',last_name='admin',
            password='adminpass',user_type=User.Types.ADMINISTRATOR)
        token = AuthToken.objects.create(user=admin_user)
        return {
            'user' : admin_user,
            'token' : token[1]
        }

    def create_dummy_student(self):
        """
        returns a dictionary containing the student user data, account data and the token.
        """
        student_user = User.objects.create_user(email='student@me.com',first_name='student',last_name='student',
            password='studentpass',user_type=User.Types.STUDENT)
        student_account = Student.objects.create(user=student_user,section=self.section1,
            registration_number='151638468951',group=1)
        token = AuthToken.objects.create(user=student_user)
        return {
            'user' : student_user,
            'account' : student_account,
            'token' : token[1]
        }

    def create_dummy_teacher(self):
        """
        returns a dictionary containing the admin user data, account data and the token.
        """
        teacher_user = User.objects.create_user(email='teacher@me.com',first_name='teacher',last_name='teacher',
            password='teacherpass',user_type=User.Types.TEACHER)
        teacher_account = Teacher.objects.create(user=teacher_user,grade='MAB')
        token = AuthToken.objects.create(user=teacher_user)
        return {
            'user' : teacher_user,
            'account' : teacher_account,
            'token' : token[1]
        }

    def create_dummy_superuser(self):
        """
        returns a dictionary containing the superuser user data and the token.
        """
        super_user = User.objects.create_superuser(email='superuser@me.com',first_name='superuser',last_name='superuser',
        password='superuserpass')
        token = AuthToken.objects.create(user=super_user)
        return {
            'user' : super_user,
            'token' : token[1]
        }

    def tearDown(self):
        return super().tearDown()
