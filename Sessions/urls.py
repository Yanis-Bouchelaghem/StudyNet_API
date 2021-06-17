from django.urls import path

from .views import SessionList, SessionDetail, ReportSession

urlpatterns = [
    path('sessions/',SessionList.as_view(), name='session_list'),
    path('sessions/<int:pk>/',SessionDetail.as_view(), name='session_detail'),
    path('sessions/report/',ReportSession.as_view(), name='session_report'),
]