# This also imports the include function
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('poll_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
