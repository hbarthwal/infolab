'''
Created on Apr 24, 2013

@author: Himanshu Barthwal
'''
from pprint import pprint

from backstrom_model import BackStromExpertiseModelGenerator
from extractdata import DataExtractorFactory

'''
Reuses all of the functionalities provided by the BackstormModel
'''
class BackstromExpertImpactModelGenerator:
    
    _expertiseDataExtractor = None
    _dataDirectory = ''
    _expertImpactModels = {}
    
    def __init__(self, dataDirectory):
        self._dataDirectory = dataDirectory
        self._expertiseDataExtractor = DataExtractorFactory.getDataExtractor('expertmodel', dataDirectory)
        
    def generateModelForExpertise(self, expertise):
        self._expertiseDataExtractor.populateData(self._dataDirectory, 'all')
        self._expertImpactModels[expertise] = {}
        print '>>>>>>>>>>> Generating models for ', expertise
        self._expertiseDataExtractor.setCurrentExpertise(expertise)
        modelGenerator = BackStromExpertiseModelGenerator(self._dataDirectory, self._expertiseDataExtractor)
        modelGenerator.generateModelForAllExpertise()
        self._expertImpactModels[expertise] = modelGenerator.getModelsForAllExpertise()
            
    def generateModelForAllExpertise(self):
        expertiseList = self._expertiseDataExtractor.getExpertiseList()
        for expertise in expertiseList:
            self.generateModelForExpertise(expertise)
        
    def displayModels(self):
        print '------- Models Generated ----'
        pprint(self._expertImpactModels)
                
                
def main():
    print 'Main'
    dataDirectory = 'expertdata/'
    modelGenerator = BackstromExpertImpactModelGenerator(dataDirectory)
    modelGenerator.generateModelForExpertise('news')
                
                
if __name__ == "__main__":
    main()       
                
                
                
                
                
                