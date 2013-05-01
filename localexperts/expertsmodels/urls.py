'''
Created on Mar 29, 2013

@author: himanshu
'''
from django.conf.urls import patterns, url
from expertsmodels.views import ExpertsHeatMapView 
from expertsmodels.views import ExpertsHeatMapService
from expertsmodels.views import ExpertSearchService
from expertsmodels.views import ExpertSearchView

urlpatterns = patterns('',
    url(r'^$', ExpertsHeatMapView.as_view()),
    url(r'^expertSearch', ExpertSearchView.as_view()),
    url(r'^getExpertSearchResults', ExpertSearchService.as_view()),
    url(r'^getExpertiseHeatmapData$', ExpertsHeatMapService.as_view(requestType = 'expertiselocations')),
    url(r'^getExpertHeatmapData$', ExpertsHeatMapService.as_view(requestType = 'expertslocations'))
)