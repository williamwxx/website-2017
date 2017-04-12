# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import url
from django.contrib import admin

# Register your models here.
class UrlAdmin(admin.ModelAdmin):
    list_display = ('host','url','key')
admin.site.register(url,UrlAdmin)