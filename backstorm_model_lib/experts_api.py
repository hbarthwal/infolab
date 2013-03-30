'''
Created on Mar 30, 2013

@author: Himanshu Barthwal
'''
from extractdata import DataExtractor

class ExpertsDataAPI:
    
    _dataDirectory = '/home/himanshu/workspace/backstorm_model_lib/heatmap/data/expert_locations'
    _data = {}

    def __init__(self):
        self._data = DataExtractor(self._dataDirectory).getExpertUsersData()
       
        
    def getExpertsHeatmapData(self, expertise):
        return self._data[expertise]
        
        
