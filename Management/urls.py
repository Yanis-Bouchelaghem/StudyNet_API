from django.urls import path
from .views import *

urlpatterns = [
    path('departments/',DepartmentList.as_view(), name='department_list'),
    path('specialties/',SpecialtyList.as_view(), name='specialty_list'),
    path('sections/',SectionList.as_view(), name='section_list'),
    path('sections/<str:pk>/',SectionDetail.as_view(), name='section_detail'),
    path('assignments/',AssignmentList.as_view(), name='Assignment_list'),
    path('modules/', ModuleList.as_view(), name='module_list'),
    path('modules/<str:pk>/', ModuleDetail.as_view(), name='module_detail'),
]