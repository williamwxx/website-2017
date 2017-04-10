# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class url(models.Model):
    host = models.CharField(max_length=254)
    url = models.CharField(max_length=254)
class json_data(models.Model):
    url = models.CharField(max_length=254)
    downtime = models.TimeField()
    json = models.TextField(max_length=3000)