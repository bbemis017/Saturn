# coding: utf-8
from django import forms
from website.models import Website,Template

class CreateSiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('domain',) 

class CreateTemplateForm(forms.ModelForm):
	class Meta:
		model = Template
		fields = ('title',)