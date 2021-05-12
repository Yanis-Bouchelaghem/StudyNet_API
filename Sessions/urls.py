from django.urls import path

from .views import SessionList

urlpatterns = [
    path('sessions/',SessionList.as_view(), name='session_list'),
]