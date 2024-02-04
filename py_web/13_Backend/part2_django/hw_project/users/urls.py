from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView)
from django.urls import path

from . import views

app_name = "app_users"

urlpatterns = [
    path("signup/", views.signupuser, name="signup"),
    path("signin/", views.loginuser, name="signin"),
    path("signout/", views.logoutuser, name="signout"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(
            template_name="app_users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="app_users/password_reset_confirm.html",
            success_url="/users/reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="app_users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
