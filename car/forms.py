#! /usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from .models import Car


class CarForm(forms.Form):
    name = forms.CharField(label="车名",error_messages={"required":"车名不能为空"})
    driver = forms.CharField(label="司机",error_messages={"required":"司机不能为空"})
    saler = forms.CharField(label="售票员",error_messages={"required":"售票员不能为空"})
    people_30 = forms.CharField(label="30元票价人数",widget=forms.NumberInput,required=False)
    people_40 = forms.CharField(label="40元票价人数",widget=forms.NumberInput,required=False)
    things = forms.CharField(label="货钱",widget=forms.NumberInput,required=False)
    food = forms.CharField(label="饭钱及其他额外花销",widget=forms.NumberInput,required=False)
    oil = forms.CharField(label="油钱",widget=forms.NumberInput,required=False)

    def clean_people_30(self):
        people_30 = self.cleaned_data.get("people_30",0)
        if people_30:
            if int(people_30) >= 60:
                raise forms.ValidationError("30元人数填写错误，不能高于60")
        return people_30

    def clean_people_40(self):
        people_40 = self.cleaned_data.get("people_40",0)
        if people_40:
            if int(people_40) >= 60:
                raise forms.ValidationError("40元人数填写错误，不能高于60")
        return people_40

    def clean_oil(self):
        oil = self.cleaned_data.get("oil",0)
        if not oil:
            oil = 0
        return oil

class DateForm(forms.Form):
    date = forms.DateField(label='运营月份',error_messages={"required":"月份不能为空"})

class RealMoneyForm(forms.Form):
    money = forms.IntegerField(label='实际收入金额',required=False)
