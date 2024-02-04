from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm

# from django.views import View



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "app_users/password_reset.html"
    email_template_name = "app_users/password_reset_email.html"
    html_email_template_name = "app_users/password_reset_email.html"
    success_url = reverse_lazy("app_users:password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "app_users/password_reset_subject.txt"


# class RegisterView(View):
#     template_name = "app_users/register.html"
#     form_class = RegisterForm
#
#     def get(self, request):
#         return render(request, self.template_name,  {"form": self.form_class} )
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data["username"]
#             messages.success(request, f"Hello, {username}. Registration successful.")
#             return redirect(to="app_user:singin")
#         return render(request, self.template_name,  {"form": form} )


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to="quotes:main")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "app_users/register.html", context={"form": form})

    return render(request, "app_users/register.html", context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to="quotes:main")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to="app_users:signin")

        login(request, user)
        return redirect(to="quotes:main")

    return render(request, "app_users/login.html", context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to="quotes:main")
