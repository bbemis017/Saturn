from __future__ import unicode_literals
from django_markdown.models import MarkdownField
from django.contrib.auth.models import User
from django.db import models
from uuslug import slugify
from website.models import Template
from section.constants import (
    Status,
    STATUS_CHOICES,
    SectionTypes
)

from time import time


class Section(models.Model):
    user = models.ForeignKey(User, null=True)
    classes = models.CharField(max_length=255, default='section')
    template = models.ForeignKey(Template)
    childType = models.IntegerField(default=SectionTypes.DEFAULT,blank=False)


def user_directory_path(instance, filename):
    return 'user/{0}/{1}'.format(instance.user.id, filename)


class Photo(Section):
    photograph = models.FileField(upload_to=user_directory_path)
    status = models.IntegerField(choices=STATUS_CHOICES, 
                                    default=Status.PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_private(self):
        return self.status == Status.PRIVATE

    @property 
    def is_public(self):
        return self.status == Status.PUBLIC 

    def __str__(self):
        return '%s' % (self.id)

    def __unicode__(self):
        return u'%s' % self.__str__()


class Summary(Section):
    content = MarkdownField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.id)

    def __unicode__(self):
        return u'%s' % self.__str__()

class Experience(Section):
    content = MarkdownField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True)
    skills = models.CharField(max_length=1024,blank=True)
    languages = models.CharField(max_length=256, blank=True)


    def __str__(self):
        return '%s' % (self.id)

    def __unicode__(self):
        return u'%s' % self.__str__()
        


class Post(Section):
    content = MarkdownField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, 
                                    default=Status.PUBLIC)
    photos = models.ManyToManyField(Photo)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_private(self):
        return self.status == Status.PRIVATE

    @property 
    def is_public(self):
        return self.status == Status.PUBLIC 

    def __str__(self):
        return '%s' % (self.id)

    def __unicode__(self):
        return u'%s' % self.__str__()
