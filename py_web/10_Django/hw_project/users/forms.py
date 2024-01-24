from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import (CharField, EmailField, EmailInput, PasswordInput,
                          TextInput)


class RegisterForm(UserCreationForm):
    username = CharField(
        min_length=3,
        max_length=20,
        required=True,
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    # email = EmailField(min_length=4, required=True,
    #                    widget=EmailInput(attrs={"class": "form-control", "placeholder": "Email"}))
    password1 = CharField(
        min_length=3,
        max_length=50,
        required=True,
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = CharField(
        min_length=3,
        max_length=50,
        required=True,
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password"}
        ),
    )

    class Meta:
        model = User
        # fields = ('username', 'email', 'password1', 'password2')
        fields = ("username", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = CharField(
        max_length=20,
        required=True,
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    password = CharField(
        max_length=50,
        required=True,
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "password"]
