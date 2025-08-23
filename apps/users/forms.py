from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "input"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
