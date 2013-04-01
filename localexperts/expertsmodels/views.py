# Create your views here.
from django.http import HttpResponse
from django.template import loader, Context
from django.views.generic import View
from expertsmodels.api.experts_api import ExpertsDataAPI
from json import dumps
from rest_framework.decorators import APIView
from rest_framework.response import Response 



class ExpertsView(View):
    
    def get(self, request):
        return self.getHeatmap(request)   
    
    
    def getHeatmap(self, request):
        template = loader.get_template('heatmap.html')
        return HttpResponse(template.render(Context({'dummy':None})))


class ExpertsService(APIView):
    
    requestType = ''
    expertLocationsJson = {}
    expertsAPIObject = ExpertsDataAPI()
    HEATMAP = 'heatmap:'
    
    def getHeatMapKey(self, expertise):
        return self.HEATMAP + expertise
    
    def _fetchData(self, request):
        self.expertsAPIObject.loadData()
        
        
    def get(self, request):
        self._fetchData(request)
        expertise = request.REQUEST['expertise']
        if self.requestType == 'expertslocations':
            return self.getUserLocationsForExpertise(request, expertise)   
    
    def getUserLocationsForExpertise(self, request, expertise):
        if self._isAvailableInCache(request, expertise):
            cachedData = self._getCacheData(request, expertise)
            return Response(cachedData)
        else :
            print 'Data not found'
        print 'Getting expertise heatmap data for ', expertise
        expertsLocations = self.expertsAPIObject.getExpertsHeatmapData(expertise)
        jsonData = dumps(expertsLocations)
        self._cacheData(request, expertise, jsonData)
        return Response(jsonData)
    
    def _isAvailableInCache(self, request, expertise):
        key = self.getHeatMapKey(expertise)
        return key in request.session
    
    def _cacheData(self, request, expertise, data):
        key = self.getHeatMapKey(expertise)
        print 'Caching data for key', key
        request.session[key] = data
    
    def _getCacheData(self, request, expertise):
        key = self.getHeatMapKey(expertise)
        print 'Getting data from cache for key', key
        return request.session[key]
    