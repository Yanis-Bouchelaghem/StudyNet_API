from django.urls import path
from .views import DepartmentList,SpecialtyList,SectionList

urlpatterns = [
    path('departments/',DepartmentList.as_view(), name='department_list'),
    path('specialties/',SpecialtyList.as_view(), name='specialty_list'),
    path('sections/',SectionList.as_view(), name='section_list'),
]