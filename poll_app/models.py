#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime

from django.db import models

__author__ = "Gennadiy Zlobin"
__credits__ = ["Gennadiy Zlobin"]
__version__ = "0.0.1"
__maintainer__ = "Gennadiy Zlobin"
__email__ = "gennad.zlobin@gmail.com"
__status__ = "Developing"

class Poll(models.Model):
    """Model for poll representing."""
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',
            default=datetime.datetime.now, blank=True)
    is_active = models.BooleanField('is active')
    def is_active_poll(self):
        return self.is_active
    is_active_poll.short_description = u'Активный опрос?'
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    """Model for choice representing. Has foreign key to poll."""
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice
