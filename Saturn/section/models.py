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


class Section(models.Model):
    unique_name = models.SlugField(max_length=255, unique=True, 
                                    blank=True, editable=False)
    alias = models.SlugField(max_length=255, blank=True)
    title = models.CharField(max_length=255, unique=True)
    classes = models.CharField(max_length=255, default='section')
    template = models.ForeignKey(Template)
    childType = models.IntegerField(default=SectionTypes.DEFAULT,blank=False)

    def save(self, *args, **kwargs):
        self.unique_name = slugify(self.title)
        if self.alias:
            self.alias = slugify(self.alias)
        else:
            self.alias = ''
        super(Section, self).save(*args, **kwargs)


def user_directory_path(instance, filename):
    return 'user/{0}/{1}'.format(instance.user.id, filename)


class Photo(Section):
    author = models.ForeignKey(User, blank=True)
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
        return '%s %s' % (self.id, self.title)

    def __unicode__(self):
        return u'%s' % self.__str__()


class Post(Section):
    author = models.ForeignKey(User, blank=True)
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
        return '%s %s' % (self.id, self.title)

    def __unicode__(self):
        return u'%s' % self.__str__()
