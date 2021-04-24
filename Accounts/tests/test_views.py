from django.urls import reverse
from rest_framework import status

from .test_setup import TestSetup

class TestUserRegister(TestSetup):
    """
    Unit tests for the registration of users through the API.
    """
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
        result = self.client.post(url,self.student_data)
        self.assertEqual(result.status_code,status.HTTP_201_CREATED)

    def test_teacher_register_anonymous(self):
        """
        Ensures that we cannot create a teacher account if we are not authenticated.
        """
        url = reverse('teacher_list')
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_teacher_register_student(self):
        """
        Ensures that a student cannot create a teacher account.
        """
        url = reverse('teacher_list')
        student = self.create_dummy_student()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + student['token'])
        result = self.client.post(url,self.teacher_data)
        self.assertEqual(result.status_code,status.HTTP_403_FORBIDDEN)

    def test_teacher_register_teacher(self):
        """
        Ensures that a teacher cannot create another teacher account.
        """
        url = reverse('teacher_list')
        teacher = self.create_dummy_teacher()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + teacher['token'])
        result = self.client.post(url,self.teacher_data)
        self.assertEqual(result.status_code,status.HTTP_403_FORBIDDEN)

    def test_teacher_register_admin(self):
        """
        Ensures that an admin can create a teacher account.
        """
        url = reverse('teacher_list')
        admin = self.create_dummy_admin()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin['token'])
        result = self.client.post(url,self.teacher_data)
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