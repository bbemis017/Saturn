from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Account(modles.Model):
	user = models.ForeignKey(User)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	bday = models.DateField(max_length=30)
	job = models.CharField(max_length=30)




