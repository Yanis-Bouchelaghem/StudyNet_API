from django.urls import path
from .views import StudentList,TeacherList,Login,GetUserData,IsEmailAvailable,TeacherDetail
from knox import views as knox_views

urlpatterns = [
    path('students/',StudentList.as_view(), name='student_list'),
    path('teachers/',TeacherList.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/',TeacherDetail.as_view(), name='teacher_detail'),
    path('login/',Login.as_view(), name='login'),
    path('user_data/',GetUserData.as_view(), name='get_user_data'),
    path('check_email/',IsEmailAvailable.as_view(), name='check_email'),
    path('logout/',knox_views.LogoutView.as_view(),name='knox_logout'),
    path('logoutall/',knox_views.LogoutAllView.as_view(),name='knox_logout_all'),

]