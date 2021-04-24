from django.urls import path
from .views import StudentList,TeacherList,Login
from knox import views as knox_views

urlpatterns = [
    path('students/',StudentList.as_view(), name='student_list'),
    path('teachers/',TeacherList.as_view(), name='teacher_list'),
    path('login/',Login.as_view(), name='login'),
    path('logout/',knox_views.LogoutView.as_view(),name='knox_logout'),
    path('logoutall/',knox_views.LogoutAllView.as_view(),name='knox_logout_all'),
]