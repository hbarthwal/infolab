'''
Created on Apr 24, 2013

@author: Himanshu Barthwal
'''

from pprint import pprint
from operator import itemgetter

from backstrom_model import BackStromExpertiseModelGenerator
from extractdata import DataExtractorFactory
from modelstore import modelsDict
from utility import Utility
from settings import Settings

'''
Reuses all of the functionalities provided by the BackstormModel
'''
class BackstromExpertImpactModelGenerator:
    
    _expertDataExtractor = None
    _dataDirectory = ''
    _expertImpactModels = {}
    
    
    def __init__(self, dataDirectory, cachedModelsFileName = ''):
        self._cachedModelsFileName = cachedModelsFileName
        self._dataDirectory = dataDirectory
        self._expertDataExtractor = DataExtractorFactory.getDataExtractor('expertmodel', dataDirectory)
        
    def generateModelForExpertise(self, expertise):
        self._expertDataExtractor.populateData(self._dataDirectory, 'all')
        self._expertImpactModels[expertise] = {}
        print '>>>>>>>>>>> Generating models for ', expertise
        self._expertDataExtractor.setCurrentExpertise(expertise)
        modelGenerator = BackStromExpertiseModelGenerator(self._dataDirectory, self._expertDataExtractor)
        modelGenerator.generateModelForAllExpertise()
        self._expertImpactModels[expertise] = modelGenerator.getModelsForAllExpertise()
            
    def generateModelForAllExpertise(self):
        expertiseList = self._expertDataExtractor.getExpertiseList()
        for expertise in expertiseList:
            self.generateModelForExpertise(expertise)
        
    def displayModels(self):
        print '------- Models Generated ----'
        pprint(self._expertImpactModels)
        
    def loadCachedModels(self):
        self._expertImpactModels = modelsDict
        
    def getExpertImpactModels(self):
        return self._expertImpactModels

class ExpertImpactAPI:
    _expertModelsDict = {}
    _modelGenerator = None
    
    def __init__(self, dataDirectory, cacheFileName):
        self._modelGenerator = BackstromExpertImpactModelGenerator(dataDirectory, cacheFileName) 
    
    def getRankedExperts(self, expertise, userLocation):
        if len(self._expertModelsDict) == 0:
            self._modelGenerator.loadCachedModels()
        self._expertModelsDict = self._modelGenerator.getExpertImpactModels()[expertise]
            
        expertImpactList = []
        for expert in self._expertModelsDict:
            models = self._expertModelsDict[expert]
            modelValue = 0
            prevModelValue = 0
            for model in models:
                modelValue = Utility.getModelValue(model, userLocation, True)
                modelValue = max(modelValue, prevModelValue)
                prevModelValue = modelValue
            expertImpactList.append((modelValue, expert))
        rankedExpertsData = sorted(expertImpactList, key = itemgetter(0), reverse = True)
        rankedExperts = []
        print rankedExpertsData
        for rankedExpertData in rankedExpertsData:
            rankedExperts.append(rankedExpertData[1])
        return rankedExperts
                        
                
def main():
    print 'Main'
    dataDirectory = 'expertdata/'
    cacheFile = 'models.json'
    expertAPI = ExpertImpactAPI(dataDirectory, cacheFile)
    #print expertAPI.getRankedExperts('travel', (27, -76))
    modelGenerator = BackstromExpertImpactModelGenerator(dataDirectory)
    modelGenerator.generateModelForExpertise('travel')
                
                
if __name__ == "__main__":
    main()       
                
                
                
                
                
                