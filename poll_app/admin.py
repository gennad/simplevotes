#!/usr/bin/env python
# -*- coding: utf8 -*-

from models import Poll
from django.contrib import admin
from poll_app.models import Choice

__author__ = "Gennadiy Zlobin"
__credits__ = ["Gennadiy Zlobin"]
__version__ = "0.0.1"
__maintainer__ = "Gennadiy Zlobin"
__email__ = "gennad.zlobin@gmail.com"
__status__ = "Developing"

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question', 'is_active']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'is_active_poll')

admin.site.register(Poll, PollAdmin)
