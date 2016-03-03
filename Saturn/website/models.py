from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Website(models.Model):
    user = models.ForeignKey(User)
    path = models.CharField(max_length=50,null=True,blank=True)
    domain = models.CharField(max_length=50)

    created_at = models.DateTimeField(default=timezone.now)


class Section(models.Model):
    heading = models.CharField(max_length=550)
    paragraph = models.CharField(max_length=1000)
    classes = models.CharField(max_length=250)

