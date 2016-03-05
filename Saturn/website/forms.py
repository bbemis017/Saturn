# coding: utf-8
from django import forms
from website.models import Website

class CreateSiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('domain','path') 
