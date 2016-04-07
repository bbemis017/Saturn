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
import json


class Section(models.Model):
    user = models.ForeignKey(User, null=True)
    classes = models.CharField(max_length=255, default='section')
    template = models.ForeignKey(Template, null=True, blank=True)
    title = models.CharField(max_length=150, default='section')


def user_directory_path(instance, filename):
    return 'static/user/{0}/{1}'.format(instance.user.id, filename)


class File(Section):
    content = models.FileField(upload_to=user_directory_path)
    status = models.IntegerField(choices=STATUS_CHOICES, 
                                    default=Status.PUBLIC)
    preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_private(self):
        return self.status == Status.PRIVATE

    @property 
    def is_public(self):
        return self.status == Status.PUBLIC 

    # WEAK WAY
    def get_filename(self):
        return self.content.name.split('/')[-1]

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

class Introduction(Section):
    created_at = models.DateTimeField(auto_now_add=True)
    education = models.CharField(max_length=255,blank=True)
    majors = models.CharField(max_length=1024,blank=True)
    languages = models.CharField(max_length=1024,blank=True)
    gpa = models.CharField(max_length=5)

    def setMajors(self, m):
        self.majors = json.dumps(m)

    '''returns python list of majors or returns false
    if there are no majors'''
    def getMajors(self):
        m = '' 
        try:
            m = json.loads(self.majors)
        except ValueError, e:
            return False
        #if there are no majors
        if len(m) == 1 and m[0] == '':
            return False
        else:
            return m

    def setLanguages(self, m):
        self.languages = json.dumps(m)

    '''returns python list of languages or returns false if there are
    no languages'''
    def getLanguages(self):
        l = ''
        try:
            l = json.loads(self.languages)
        except ValueError, e:
            return False
        if len(l) == 1 and l[0] == '':
            return False
        else:
            return l

class Experience(Section):
    content = MarkdownField(blank=True,null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    skills = models.CharField(max_length=1024,blank=True)


    def __str__(self):
        return '%s' % (self.id)

    def __unicode__(self):
        return u'%s' % self.__str__()


    def setSkills(self, s):
        self.skills = json.dumps(skills)

    #returns python list of skills or returns false if there are no skills
    def getSkills(self):
        s = ''
        try:
            s = json.loads(self.skills)
        except ValueError, e:
            return False
        #if there are no skills
        if len(s) == 1 and s[0] == '':
            return False
        else:
            return s
        


class Post(Section):
    content = MarkdownField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, 
                                    default=Status.PUBLIC)
    file = models.ManyToManyField(File)
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
