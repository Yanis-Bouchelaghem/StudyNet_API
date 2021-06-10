from django.urls import path
from.views import AppVersionCheckView,TestFCM
urlpatterns = [
    path('appversion/',AppVersionCheckView.as_view(),name='app_version_check'),
    path('testFCM/',TestFCM.as_view(),name='test_fcm'),
]
