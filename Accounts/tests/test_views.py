from django.urls import reverse
from rest_framework import status

from .test_setup import TestSetup
from Accounts.models import User,Student,Teacher
class TestUserRegister(TestSetup):
    """
    Unit tests for the registration of users through the API.
    """
    def test_student_retrieve(self):
        """
        Ensures that we can retrieve all students.
        """
        #Create a few students just for this specific test.
        student_user1 = User.objects.create_user(email='student1@me.com',first_name='student',last_name='student',
            password='studentpass',user_type=User.Types.STUDENT)
        student_user2 = User.objects.create_user(email='student2@me.com',first_name='student',last_name='student',
            password='studentpass',user_type=User.Types.STUDENT)
        student_user3 = User.objects.create_user(email='student3@me.com',first_name='student',last_name='student',
            password='studentpass',user_type=User.Types.STUDENT)
        Student.objects.create(user=student_user1,section=self.section1,
            registration_number='151638468951',group=1)
        Student.objects.create(user=student_user2,section=self.section2,
            registration_number='151638468951',group=1)
        Student.objects.create(user=student_user3,section=self.section1,
            registration_number='151638468951',group=1)

        url = reverse('student_list')
        #We expect to retrieve all student accounts.
        result = self.client.get(url)
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Student.objects.all().count())
        #Deactivate a student then retrieve again, we expect to retrieve even the deactivated accounts.
        student_user1.is_active = False
        student_user1.save()
        result = self.client.get(url)
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Student.objects.all().count())

    def test_student_by_section_retrieve(self):
        """
        Ensures that we can retrieve students based on section.
        """
        #Create a student
        self.create_dummy_student()
        url = reverse('student_list')
        #Test filter by an existing section
        result = self.client.get(url,{'section':self.section1.code})
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Student.objects.filter(section=self.section1.code).count())
        #Test filter by a non existent section
        result = self.client.get(url,{'section':'NonExistent'})
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Student.objects.filter(section='NonExistent').count())

    def test_teacher_retrieve_anonymous(self):
        """
        Ensures that a token is required to retrieve teachers.
        """
        url = reverse('teacher_list')
        result = self.client.get(url)
        self.assertEqual(result.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_teacher_retrieve(self):
        """
        Ensures that we can retrieve all teachers.
        """
        #Create a few teachers just for this test.
        teacher_user1 = User.objects.create_user(email='teacher1@me.com',first_name='teacher',last_name='teacher',
            password='teacherpass',user_type=User.Types.TEACHER)
        teacher_user2 = User.objects.create_user(email='teacher2@me.com',first_name='teacher',last_name='teacher',
            password='teacherpass',user_type=User.Types.TEACHER)
        teacher_user3 = User.objects.create_user(email='teacher3@me.com',first_name='teacher',last_name='teacher',
            password='teacherpass',user_type=User.Types.TEACHER)
        Teacher.objects.create(user=teacher_user1,grade='MAB')
        Teacher.objects.create(user=teacher_user2,grade='MAA')
        Teacher.objects.create(user=teacher_user3,grade='MCB')

        url = reverse('teacher_list')
        #Use a student token for retrieval.
        student = self.create_dummy_student()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + student['token'])
        #We expect to retrieve all teacher accounts.
        result = self.client.get(url)
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Teacher.objects.all().count())
        #Deactivate a teacher then retrieve again, we expect to retrieve even the deactivated accounts.
        teacher_user1.is_active = False
        teacher_user1.save()
        result = self.client.get(url)
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Teacher.objects.all().count())

    def test_student_register_no_data(self):
        """
        Ensures that we cannot create a student account with no data.
        """
        url = reverse('student_list')
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_400_BAD_REQUEST)

    def test_student_register(self):
        """
        Ensures that we can create a student account with valid data.
        """
        url = reverse('student_list')
        result = self.client.post(url,self.valid_student_data)
        self.assertEqual(result.status_code,status.HTTP_201_CREATED)

    def test_teacher_register_anonymous(self):
        """
        Ensures that a token is required to create a teacher account.
        """
        url = reverse('teacher_list')
        result = self.client.post(url,self.valid_teacher_data)
        self.assertEqual(result.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_teacher_register_student(self):
        """
        Ensures that a student cannot create a teacher account.
        """
        url = reverse('teacher_list')
        student = self.create_dummy_student()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + student['token'])
        result = self.client.post(url,self.valid_teacher_data)
        self.assertEqual(result.status_code,status.HTTP_403_FORBIDDEN)

    def test_teacher_register_teacher(self):
        """
        Ensures that a teacher cannot create another teacher account.
        """
        url = reverse('teacher_list')
        teacher = self.create_dummy_teacher()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + teacher['token'])
        result = self.client.post(url,self.valid_teacher_data)
        self.assertEqual(result.status_code,status.HTTP_403_FORBIDDEN)

    def test_teacher_register_admin(self):
        """
        Ensures that an admin can create a teacher account.
        """
        url = reverse('teacher_list')
        admin = self.create_dummy_admin()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin['token'])
        result = self.client.post(url,self.valid_teacher_data)
        self.assertEqual(result.status_code,status.HTTP_201_CREATED)

class TestLogin(TestSetup):
    """
    Unit tests for logging in through the API.
    """
    def test_login_anonymous(self):
        """
        Ensures that logging in with no/wrong credentials is refused.
        """
        url = reverse('login')
        #Test no credentials.
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_400_BAD_REQUEST)
        #Test wrong credentials.
        wrong_credentials = {'email':'wrongemail@me.com','password':'wrongpassword'}
        result = self.client.post(url,wrong_credentials)
        self.assertEqual(result.status_code,status.HTTP_400_BAD_REQUEST)

    def test_login_student(self):
        """
        Ensures that the login view returns the student and a token when logging in with
        a student account credentials.
        """
        url = reverse('login')
        student = self.create_dummy_student()
        credentials = {'email':student['user'].email,'password':'studentpass'}
        result = self.client.post(url,credentials)
        self.assertEqual(result.status_code,status.HTTP_201_CREATED)

    def test_login_teacher(self):
        """
        Ensures that the login view returns the teacher and a token when logging in with
        a teacher account credentials.
        """
        url = reverse('login')
        teacher = self.create_dummy_teacher()
        credentials = {'email':teacher['user'].email,'password':'teacherpass'}
        result = self.client.post(url,credentials)
        self.assertEqual(result.status_code,status.HTTP_201_CREATED)

    def test_login_superuser(self):
        """
        Ensures that logging in with a superuser is refused.
        """
        url = reverse('login')
        superuser = self.create_dummy_superuser()
        credentials = {'email':superuser['user'].email,'password':'superuserpass'}
        result = self.client.post(url,credentials)
        self.assertEqual(result.status_code,status.HTTP_400_BAD_REQUEST)

class TestLogout(TestSetup):
    """
    Unit tests for logging out through the API.
    """
    def test_logout_no_credentials(self):
        """
        Ensures that logging out with no/wrong credentials is refused.
        """
        url = reverse('knox_logout')
        #Test with no credentials
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_401_UNAUTHORIZED)
        #Test with wrong credentials
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'wrongtoken')
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_logout_student(self):
        """
        Ensures that a student is able to logout.
        """
        url = reverse('knox_logout')
        student = self.create_dummy_student()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + student['token'])
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_204_NO_CONTENT)

    def test_logout_teacher(self):
        """
        Ensures that a teacher is able to logout.
        """
        url = reverse('knox_logout')
        teacher = self.create_dummy_teacher()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + teacher['token'])
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_204_NO_CONTENT)

    def test_logout_admin(self):
        """
        Ensures that an admin is able to logout.
        """
        url = reverse('knox_logout')
        admin = self.create_dummy_admin()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin['token'])
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_204_NO_CONTENT)

class TestLogoutAll(TestSetup):
    """
    Unit tests for logging out all tokens through the API.
    """
    def test_logout_all_no_credentials(self):
        """
        Ensures that logging out with no/wrong credentials is refused.
        """
        url = reverse('knox_logout_all')
        #Test with no credentials
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_401_UNAUTHORIZED)
        #Test with wrong credentials
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'wrongtoken')
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_logout_all_student(self):
        """
        Ensures that a student is able to logout all tokens.
        """
        url = reverse('knox_logout')
        student = self.create_dummy_student()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + student['token'])
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_204_NO_CONTENT)

    def test_logout_teacher(self):
        """
        Ensures that a teacher is able to logout all tokens.
        """
        url = reverse('knox_logout_all')
        teacher = self.create_dummy_teacher()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + teacher['token'])
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_204_NO_CONTENT)

    def test_logout_admin(self):
        """
        Ensures that an admin is able to logout all tokens.
        """
        url = reverse('knox_logout_all')
        admin = self.create_dummy_admin()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin['token'])
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_204_NO_CONTENT)
