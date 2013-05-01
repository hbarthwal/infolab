@author: Himanshu Barthwal
@revision : Preeti Suman

# Create your views here.
from django.http import HttpResponse
from django.template import loader, Context
from django.views.generic import View
from expertsmodels.api.experts_api import ExpertsDataAPI
from expertsmodels.api.experts_api import ExpertsSearchAPI 
from json import dumps
from rest_framework.decorators import APIView
from rest_framework.response import Response 

'''
This view provides the template for expert search page
'''
class ExpertSearchView(View):
    
    def get(self, request):
        return self.getExpertSearch(request)
    
    def getExpertSearch(self, request):
        template = loader.get_template('expertSearch.html')
        return HttpResponse(template.render(Context({'dummy':None})))
    
'''
This view provides all the web services for the expert search page.
'''
class ExpertSearchService(APIView):
    _expertSearchAPI = ExpertsSearchAPI()
    
    def get(self, request):
        query = request.REQUEST['query']
        userLocation = request.REQUEST['userlocation']
        coordinates = userLocation.split(',')
        userLocation = (float(coordinates[0]), float(coordinates[1]))
        results = self._expertSearchAPI.getExperts(query, userLocation)
        jsonData = dumps(results)
        return Response(jsonData) 
'''
This view serves the page for the heatmap page.
'''        
class ExpertsHeatMapView(View):
    def get(self, request):
        return self.getExpertiseHeatmap(request)   
    
    
    def getExpertiseHeatmap(self, request):
        template = loader.get_template('heatmap.html')
        return HttpResponse(template.render(Context({'dummy':None})))

'''
This view provides the webservices for the heatmap page.
'''   
class ExpertsHeatMapService(APIView):
    requestType = ''
    expertLocationsJson = {}
    expertsAPIObject = ExpertsDataAPI()
    HEATMAP = 'heatmap:'
    
    def getHeatMapKey(self, expertise, expertId = ''):
        return self.HEATMAP + expertise + expertId
    
        
    def get(self, request):
        print 'Got request inside get function'
        expertise, expertId = '', ''
        if 'expertise' in request.REQUEST:
            expertise = request.REQUEST['expertise']
        if 'expertId' in request.REQUEST:
            expertId = request.REQUEST['expertId']
        if self.requestType == 'expertiselocations':
            return self.getUserLocationsForExpertise(request, expertise)   
        if self.requestType == 'expertslocations':
            return self.getUserLocationsForExpert(request, expertise, expertId)   
    
    def getUserLocationsForExpertise(self, request, expertise):
        if self._isAvailableInCache(request, expertise):
            cachedData = self._getCacheData(request, expertise)
            return Response(cachedData)
        else :
            print 'Data not found'
        print 'Getting expertise heatmap data for ', expertise
        expertsLocations = self.expertsAPIObject.getExpertiseHeatmapData(expertise)
        jsonData = dumps(expertsLocations)
        self._cacheData(request, expertise, jsonData)
        return Response(jsonData)
    
    
    def getUserLocationsForExpert(self, request, expertise, expertId):
        print 'Executing -- getUserLocationsForExpert'
        if self._isAvailableInCache(request, expertise + expertId):
            cachedData = self._getCacheData(request, expertise, expertId)
            return Response(cachedData)
        else :
            print 'Data not found'
        print 'Getting expert heatmap data for ', expertise, '-', expertId
        expertsLocations = self.expertsAPIObject.getExpertHeatmapData(expertise, expertId)
        jsonData = dumps(expertsLocations)
        self._cacheData(request, expertise + expertId, jsonData)
        return Response(jsonData)
    
    def _isAvailableInCache(self, request, expertise, expertId = ''):
        key = self.getHeatMapKey(expertise, expertId)
        return key in request.session
    
    def _cacheData(self, request, expertise, data):
        key = self.getHeatMapKey(expertise)
        print 'Caching data for key', key
        request.session[key] = data
    
    def _getCacheData(self, request, expertise, expertId = ''):
        key = self.getHeatMapKey(expertise, expertId)
        print 'Getting data from cache for key', key
        return request.session[key]
    
