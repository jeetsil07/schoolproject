from django.contrib import admin
from django.urls import path, include
from account.views import UserLoginView, UserPasswordChangeView, UserProfileView, UserRegistrationView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(),name="user-registration"),
    path("login/", UserLoginView.as_view(),name="user-login"),
    path("profile/", UserProfileView.as_view(),name="user-profile"),
    path("changepassword/", UserPasswordChangeView.as_view(),name="user-password-change"),
]
