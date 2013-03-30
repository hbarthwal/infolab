'''
Created on Mar 29, 2013

@author: himanshu
'''
from django.conf.urls import patterns, url

from expertsmodels.views import ExpertsView 
from expertsmodels.views import ExpertsService

urlpatterns = patterns('',
    url(r'^$', ExpertsView.as_view()),
    url(r'^getHeatmapData$', ExpertsService.as_view(requestType = 'expertslocations'))
)