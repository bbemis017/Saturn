# coding: utf-8
from django import forms
from section.models import create_summary

class summaryForm(forms.ModelForm):
   class Meta:
       model = Section
       fields = ('domain') 
