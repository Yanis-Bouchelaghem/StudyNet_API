from django.urls import path
from .views import StudentList,TeacherList,Login

urlpatterns = [
    path('students/',StudentList.as_view()),
    path('teachers/',TeacherList.as_view()),
    path('login/',Login.as_view()),
]