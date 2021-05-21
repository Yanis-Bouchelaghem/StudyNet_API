from django.urls import path

from .views import HomeworkList

urlpatterns = [
    path('homeworks/',HomeworkList.as_view(), name='homework_list'),
]