from django.contrib import admin
from django.urls import path, include
from account.views import UserLoginView, UserPasswordChangeView, UserProfileView, UserRegistrationView, UsersdetailsView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(),name="user-registration"),
    path("login/", UserLoginView.as_view(),name="user-login"),
    path("profile/", UserProfileView.as_view(),name="user-profile"),
    path("changepassword/", UserPasswordChangeView.as_view(),name="user-password-change"),
    path("details/", UsersdetailsView.as_view(),name="user-details"),
]
