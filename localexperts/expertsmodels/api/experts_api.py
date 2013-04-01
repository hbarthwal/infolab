'''
Created on Mar 30, 2013

@author: Himanshu Barthwal
'''
from expertsmodels.lib.extractdata import DataExtractor

class ExpertsDataAPI:
    
    _dataDirectory = '/home/himanshu/workspace/infolab/localexperts/expertsmodels/lib/data/expert_locations'

    def loadData(self):
        print 'Loading the experts users data'
        self._data = DataExtractor(self._dataDirectory)
       
    
    def getExpertsHeatmapData(self, expertise):
        dataExtractor = DataExtractor(self._dataDirectory)
        expertsDataList = dataExtractor.getExpertUsersData(expertise)
        print 'No of entries : ', len(expertsDataList)
        expertsDataListForHeatmap = []
        for expertData in expertsDataList:
            expertDataDict = {'lat': expertData[2],'lng':expertData[3], 'count':1}
            expertsDataListForHeatmap.append(expertDataDict)
        return expertsDataListForHeatmap
        
        
