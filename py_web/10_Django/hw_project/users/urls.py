from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from . import views
from .forms import LoginForm

app_name = "app_users"

urlpatterns = [
    path("signup/", views.signupuser, name="signup"),
    path("signin/", views.loginuser, name="signin"),
    path("signout/", views.logoutuser, name="signout"),
]
