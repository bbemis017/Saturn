# coding: utf-8
from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SigninForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email", max_length=255)
    password = forms.CharField(label="Password", max_length=100, widget = forms.PasswordInput)


class ForgetForm(forms.Form):
    email = forms.EmailField(label="Email")


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", max_length=255, widget = forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", max_length=255, widget = forms.PasswordInput)
    verification_code = forms.CharField(label="verification_code", max_length=255)
