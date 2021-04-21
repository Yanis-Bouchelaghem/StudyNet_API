from django.urls import path
from .views import StudentList,TeacherList

urlpatterns = [
    path('students/',StudentList.as_view()),
    path('teachers/',TeacherList.as_view())
]