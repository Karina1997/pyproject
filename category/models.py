# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{}'.format(self.name)