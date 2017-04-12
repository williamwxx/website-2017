# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class url(models.Model):
    host = models.CharField(max_length=254)
    url = models.CharField(max_length=254)
    key = models.CharField(max_length=254)
class json_data(models.Model):
    url = models.CharField(max_length=254)
    ip_info = models.CharField(max_length=254)
    downtime = models.CharField(max_length=50)
    json = models.TextField(max_length=3000)
class ip_json_data(models.Model):
    url = models.CharField(max_length=254)
    ip = models.CharField(max_length=50)
    downtime = models.CharField(max_length=50)
    ip_json = models.TextField(max_length=3000)
