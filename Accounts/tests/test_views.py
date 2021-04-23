from django.urls import reverse
from rest_framework import status

from .test_setup import TestSetup

class TestViews(TestSetup):

    def test_student_register_no_data(self):
        """
        Ensures that we cannot create a student account with no data.
        """
        url = reverse('student-list')
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_400_BAD_REQUEST)

    def test_student_register(self):
        """
        Ensures that we can create a student account with valid data.
        """
        url = reverse('student-list')
        result = self.client.post(url,self.student_data)
        self.assertEqual(result.status_code,status.HTTP_201_CREATED)

    def test_teacher_register_anonymous(self):
        """
        Ensures that we cannot create a teacher account if we are not authenticated.
        """
        url = reverse('teacher-list')
        result = self.client.post(url)
        self.assertEqual(result.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_teacher_register_student(self):
        """
        Ensures that a student cannot create a teacher account.
        """
        url = reverse('teacher-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student_user_token[1])
        result = self.client.post(url,self.teacher_data)
        self.assertEqual(result.status_code,status.HTTP_403_FORBIDDEN)

    def test_teacher_register_teacher(self):
        """
        Ensures that a teacher cannot create another teacher account.
        """
        url = reverse('teacher-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher_user_token[1])
        result = self.client.post(url,self.teacher_data)
        self.assertEqual(result.status_code,status.HTTP_403_FORBIDDEN)

    def test_teacher_register(self):
        """
        Ensures that an admin can create a teacher account.
        """
        url = reverse('teacher-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token[1])
        result = self.client.post(url,self.teacher_data)
        self.assertEqual(result.status_code,status.HTTP_201_CREATED)
