#! /usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=15,error_messages={"required":"用户名不能为空"})
    password = forms.CharField(label="密码" , widget=forms.PasswordInput, max_length=15, min_length=6,error_messages={"required":"密码不能为空"})

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="密码",widget=forms.PasswordInput, max_length=15)
    password2 = forms.CharField(label="确认密码",widget=forms.PasswordInput, max_length=15)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("密码不匹配")
        return cd["password2"]

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth','photo')