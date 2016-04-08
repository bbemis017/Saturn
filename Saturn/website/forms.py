# coding: utf-8
from django import forms
from website.models import Website, Template, ResumeTemplate, CourseTemplate 

class CreateSiteForm(forms.ModelForm):
   class Meta:
       model = Website
       fields = ('domain','description') 

class CreateTemplateForm(forms.ModelForm):
   class Meta:
        model = Template
        fields = ('title',)

class CreateResumeTemplateForm(forms.ModelForm):
    class Meta:
        model = ResumeTemplate
        fields = ('author',)

class DeleteSiteForm(forms.ModelForm):
	class Meta:
		model = Website
		fields = ('domain',)

class CreateCourseTemplateForm(forms.ModelForm):
  class Meta:
    model = CourseTemplate
    fields = ('author',)
