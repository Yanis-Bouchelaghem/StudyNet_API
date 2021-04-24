from django.urls import path
from.views import AppVersionCheckView
urlpatterns = [
    path('appversion/',AppVersionCheckView.as_view(),name='app_version_check'),
]
