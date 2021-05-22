from django.urls import path

from .views import HomeworkDetail, HomeworkList

urlpatterns = [
    path('homeworks/',HomeworkList.as_view(), name='homework_list'),
    path('homeworks/<int:pk>/', HomeworkDetail.as_view(), name='homework_detail'),
]