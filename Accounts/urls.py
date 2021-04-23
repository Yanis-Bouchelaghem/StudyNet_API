from django.urls import path
from .views import StudentList,TeacherList,Login

urlpatterns = [
    path('students/',StudentList.as_view(), name='student-list'),
    path('teachers/',TeacherList.as_view(), name='teacher-list'),
    path('login/',Login.as_view(), name='login'),
]