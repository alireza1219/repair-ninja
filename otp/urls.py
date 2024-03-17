from django.urls import path

from . import views


urlpatterns = [
    path('email/', views.UserOTPCreateViewSet.as_view()),
    path('email/verify/', views.UserOTPVerifyViewSet.as_view()),
]
