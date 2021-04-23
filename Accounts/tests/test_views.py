from .test_setup import TestSetup
from django.urls import reverse
from rest_framework import status

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
    