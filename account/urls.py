from django.contrib import admin
from django.urls import path, include
from account.views import UserLoginView, UserRegistrationView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(),name="user-registration"),
    path("login/", UserLoginView.as_view(),name="user-login"),
]
