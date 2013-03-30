'''
Created on Mar 29, 2013

@author: himanshu
'''
from django.conf.urls import patterns, url

from expertsmodels import views

urlpatterns = patterns('',
    url(r'^$', views.heatmap),
    url(r'^getHeatmapData$', views.getUserLocationsForExpertise)
)