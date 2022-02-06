
# Create your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Size(models.Model):
    size = models.SmallIntegerField()

    def __unicode__(self):
        return self.size