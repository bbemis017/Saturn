from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Template(models.Model):
    title = models.CharField(max_length=50)    
    path = models.CharField(max_length=50,null=True)

class ResumeTemplate(Template):
    author = models.CharField(max_length=50)

class CourseTemplate(Template):
    author = models.CharField(max_length=50)

class Website(models.Model):
    user = models.ForeignKey(User)
    domain = models.CharField(max_length=50)
    template = models.ForeignKey(Template, null=True)
    description = models.CharField(max_length=150,null=True)

    created_at = models.DateTimeField(default=timezone.now)

