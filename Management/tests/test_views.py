from django.urls import reverse
from rest_framework import status

from Management.models import Department,Specialty,Section
from .test_setup import TestSetup

class TestDepartmentsRetrieve(TestSetup):

    def test_departments_retrieve(self):
        """
        Ensures that this view is retrieving all departments.
        """
        url = reverse('department_list')
        result = self.client.get(url)
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Department.objects.all().count())

class TestSpecialtyRetrieve(TestSetup):
    def test_specialties_retrieve(self):
        """
        Ensures that this view is retrieving all specialties.
        """
        url = reverse('specialty_list')
        result = self.client.get(url)
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Specialty.objects.all().count())

    def test_specialties_by_department_retrieve(self):
        """
        Ensures that this view is retrieving specialties based on the given department.
        """
        url = reverse('specialty_list')
        #Test filter by an existing department
        result = self.client.get(url,{'department':'CS'})
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Specialty.objects.filter(Department='CS').count())
        #Test filter by a non existing department
        result = self.client.get(url,{'department':'NonExistant'})
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Specialty.objects.filter(Department='NonExistant').count())

class TestSectionRetrieve(TestSetup):
    def test_sections_retrieve(self):
        """
        Ensures that this view is retrieving all sections.
        """
        url = reverse('section_list')
        result = self.client.get(url)
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Section.objects.all().count())

    def test_specialties_by_department_retrieve(self):
        """
        Ensures that this view is retrieving sections based on the given specialty.
        """
        url = reverse('section_list')
        #Test filter by an existing department
        result = self.client.get(url,{'specialty':'GD'})
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Section.objects.filter(specialty='GD').count())
        #Test filter by a non existing department
        result = self.client.get(url,{'specialty':'NonExistant'})
        self.assertEqual(result.status_code,status.HTTP_200_OK)
        self.assertEqual(len(result.data),Section.objects.filter(specialty='NonExistant').count())
