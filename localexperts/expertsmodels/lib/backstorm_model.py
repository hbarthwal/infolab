'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
from region import Region
from extractdata import DataExtractor
from region import Region

class BackStormModelGenerator:
    
    _dictExpertiseRegions =  {'tech': Region()}
    _extractedData = DataExtractor()
    _dataDirectory = '/home/himanshu/workspace/infolab/localexperts/expertsmodels/lib/data/expert_locations'
    
    def __init__(self):
        self._extractedData.populateData(self._dataDirectory)
    

    def getMaxLikelihoodValue(self, region):
        print 'getting the max likelihood value for region', region
        
    def calculateLogLikelihood(self, region):
        print 'calculating the log likelihood value for region', region
        
    def getMaximumLikelyRegion(self, region):
        print 'calculating maximum likelihood for all regions and getting the maximum region'
    
    def createParentRegions(self):
        print 'creating parent Regions'
    
    def createParentRegion(self, expertise):
        print 'Creating region for ', expertise 
        
    
    
    
    
    
    
                     
        
         
        