from django.urls import path
from.views import AppVersionCheckView,TestFCM,RegisterTeacherFCM,UnregisterTeacherFCM
urlpatterns = [
    path('appversion/',AppVersionCheckView.as_view(),name='app_version_check'),
    path('testFCM/',TestFCM.as_view(),name='test_fcm'),
    path('registerFCM/',RegisterTeacherFCM.as_view(),name='register_fcm'),
    path('unregisterFCM/',UnregisterTeacherFCM.as_view(),name='unregister_fcm')

]
