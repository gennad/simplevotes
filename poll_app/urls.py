#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.conf.urls.defaults import patterns

__author__ = "Gennadiy Zlobin"
__credits__ = ["Gennadiy Zlobin"]
__version__ = "0.0.1"
__maintainer__ = "Gennadiy Zlobin"
__email__ = "gennad.zlobin@gmail.com"
__status__ = "Developing"

urlpatterns = patterns('poll_app.views',
    (r'^$', 'index'),
    (r'^allresults/$', 'allresults'),
    (r'^(?P<poll_id>\d+)/$', 'detail'),
    (r'^(?P<poll_id>\d+)/results/$', 'results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),

    (r'^api_allresults/$', 'api_allresults'),
    (r'^api_get/(?P<poll_id>\d+)/$', 'api_get'),
    (r'^api_results/(?P<poll_id>\d+)/results/$', 'api_results'),
    (r'^api_post/(?P<poll_id>\d+)/vote/$', 'api_post'),
)
