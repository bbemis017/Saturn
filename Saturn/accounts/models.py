from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from website.models import Website
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta


import hashlib


ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ23456789' 

class Accounts(models.Model):
    user = models.ForeignKey(User)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField('verification_code',
                                         max_length=255, blank=True, null=True)
    expire_at = models.DateTimeField('Effective time', blank=True, null=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bday = models.DateField(max_length=30, blank=True, null=True)
    job = models.CharField(max_length=30, blank=True, null=True)


    def __unicode__(self):
        return "{}'s accounts".format(self.user.username)

    def generate_verification_code(self, commit=True):
        self.verification_code = get_random_string(10, ALLOWED_CHARS) 
        self.expire_at = timezone.now() + timedelta(hours=24)
        if commit:
            self.save()

    def get_next_website_id(self):
        obj = Website.objects.filter(user=self.user).order_by('-id')
        if not obj.exists():
            return 1
        return obj[0].id + 1



User.account = property(lambda u: Accounts.objects.get_or_create(user=u)[0])
