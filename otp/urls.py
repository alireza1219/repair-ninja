from django.urls import path

from . import views


urlpatterns = [
    path('email/', views.CustomerOTPCreateViewSet.as_view()),
    path('email/verify/', views.CustomerOTPVerifyViewSet.as_view()),
]
