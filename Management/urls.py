from django.urls import path
from .views import DepartmentList,SpecialtyList,SectionList,AssignmentList,ModuleList

urlpatterns = [
    path('departments/',DepartmentList.as_view(), name='department_list'),
    path('specialties/',SpecialtyList.as_view(), name='specialty_list'),
    path('sections/',SectionList.as_view(), name='section_list'),
    path('assignments/',AssignmentList.as_view(), name='Assignment_list'),
    path('modules/', ModuleList.as_view(), name='module_list'),
]