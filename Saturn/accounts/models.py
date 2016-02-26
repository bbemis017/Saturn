from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate


import hashlib


ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ23456789' 

class Accounts(models.Model):
    user = models.ForeignKey(User)
    verified = models.BooleanField(default=False)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bday = models.DateField(max_length=30)
    job = models.CharField(max_length=30)


    def __unicode__(self):
        return "{}'s accounts".format(self.user.username)

    def generate_verification_code(self, commit=True):
        self.verification_code = get_random_string(10, ALLOWED_CHARS) 
        self.expire_at = timezone.now() + timedelta(hours=24)
        if commit:
            self.save()

    #Password verification funciton
    def authetication(self, usr, pwd) :
    	user=authenticate(username = usr, password = pwd)
    	if user is not None:
    		#return success message
    		return "log in success!"
    	else:
    		#return error message
    		return "log in failure!"