from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^expertsmodels/', include('expertsmodels.urls')),
    url(r'^expertsmodels/', include('rest_framework.urls', namespace='rest_framework')),
    )