# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.

class Comment(models.Model):
    text = models.TextField(default="")
    createdata = models.DateTimeField(auto_now_add=True)
    changedata = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey('blog.Post', related_name='comments')

    def __unicode__(self):
        return u'{} ({})'.format(self.text, self.author)