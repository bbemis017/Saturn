from __future__ import unicode_literals

from django.db import models

class Website(models.Model):
    domain = models.CharField(max_length=50)


class Section(models.Model):
    heading = models.CharField(max_length=550)
    paragraph = models.CharField(max_length=1000)
    classes = models.CharField(max_length=250)

