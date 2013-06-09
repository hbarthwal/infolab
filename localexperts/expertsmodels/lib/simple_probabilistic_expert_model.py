'''
Created on May 26, 2013

@author: himanshu
'''
from math import pow
from pprint import pprint

from extractdata import DataExtractorFactory
from utility import Utility




class SimpleProbabilisticExpertModel(object):
    '''
    This class implements the simple probabilistic expert model.
    For example: for user A: a guy in SF lists him as tech expert,
    two guys in NYC list him as tech expert, and 1 guy lists him
    as a tech expert in Austin. Then the probability for the guy
    being a tech expert in SF, NYC, and Austin are 0.25, 0.5, 0.25 
    respectively.
    '''

    _dataDirectory = ''
    _dataExtractor = None
    _Dmin = 160
    _alpha = 1.75
    _labelerStatsDict = {}
    
    '''
    Warning : These regions should not be overlapping otherwise the 
    whole thing does not make sense
    '''
    
    _regions = {
                'SF':{'center': (37.7750, -122.4183), 'radius': 100},
                'NYC': {'center': (40.7142, -74.0064), 'radius': 100}, 
                'Austin': {'center': (30.2669, -97.7428),  'radius': 100},
                'College Station': {'center': (30.6278, -96.3342), 'radius': 100},
               }
    
    # Contains the names of the expertise which are under consideration
    _expertiseList = ['tech', 'travel']
    
    # This dictionary will contain the scores for all the expert user 
    # based on our calculation.
    _expertsScoreDict = {}
    
    
    def __init__(self, dataDirectory):
        '''
        Constructor
        ''' 
        self._dataDirectory = dataDirectory
        self._dataExtractor = DataExtractorFactory.getDataExtractor('expertmodel', dataDirectory)
   
    def _getScore(self, userData, regionName):
        '''
        Calculates the score for an expert given by a user
        the score is discounted using the log10(distance)
        therefore the user far away from the expertise location
        of the expert will be ble to assign a lower score for 
        that expertise. 
        '''
        userLocation = userData[2], userData[3]
        regionCenter = self._regions[regionName]['center']
        distance = Utility.haversine(regionCenter[0], regionCenter[1], userLocation[0], userLocation[1])
        # This is the equation used for calculating the score for the
        # expert.
        score = (self._Dmin / (self._Dmin + distance))
        score = pow(score, self._alpha)
        return score

    def updateScore(self, expertise, expertId, userData):
        '''
        Updates the score in the score dictionary 
        '''
        for expertRegionName in self._regions:
            score =  self._getScore(userData, expertRegionName)
            self._updateLabelersStats(expertise, expertId, expertRegionName, userData)
            if expertise not in self._expertsScoreDict:
                self._expertsScoreDict[expertise] = {}
            
            if expertId not in self._expertsScoreDict[expertise]:
                self._expertsScoreDict[expertise][expertId] = {}
            regionScoreDict = self._expertsScoreDict[expertise][expertId]
                
            if expertRegionName not in regionScoreDict:
                regionScoreDict[expertRegionName] = score

            else:
                regionScoreDict[expertRegionName] += score
    
    def generateModel(self):
        '''
        Iterates the userdata and calculates the probability values 
        for all the experts.
        '''
        # Get all the user data from the data extractor.

        self._dataExtractor.populateData(self._dataDirectory)
        allExpertsData = self._dataExtractor.getDataCopy()
               
        # Iterate through the data and calculate the score for 
        # each expert
        for expertise in self._expertiseList:
            expertUserData = allExpertsData[expertise]
            self._expertsScoreDict[expertise] = {}
            for expertId in expertUserData:
                for labelingUserData in expertUserData[expertId]:
                    self.updateScore(expertise, expertId, labelingUserData)
        
    
    def _updateLabelersStats(self, expertise, expertId, regionName, userData):
        '''
        Generates the statistics for the labeling users 
        Calculates that what percentage of the labeling
        users lie in a certain city within in a given 
        radius.
        '''
        userLocation = userData[2], userData[3]
        region = self._regions[regionName]
        regionCenter = region['center']
        distance = Utility.haversine(regionCenter[0], regionCenter[1], userLocation[0], userLocation[1])
        
        if expertise not in self._labelerStatsDict:
            self._labelerStatsDict[expertise] = {}
            
        if expertId not in self._labelerStatsDict[expertise]:
            self._labelerStatsDict[expertise][expertId] = {}
            
            for regionName in self._regions:
                self._labelerStatsDict[expertise][expertId][regionName] = {}
                self._labelerStatsDict[expertise][expertId][regionName]['inside'] = 0
                self._labelerStatsDict[expertise][expertId][regionName]['outside'] = 0
        
        if distance < self._regions[regionName]['radius']:
            self._labelerStatsDict[expertise][expertId][regionName]['inside'] += 1
            
        else:
            self._labelerStatsDict[expertise][expertId][regionName]['outside'] += 1
    
        
def main():
    print 'Main'
    dataDirectory = 'expertdata/'
    modelGenerator = SimpleProbabilisticExpertModel(dataDirectory)
    modelGenerator.generateModel()
    pprint(modelGenerator._expertsScoreDict)
    pprint(modelGenerator._labelerStatsDict)
if __name__ == "__main__":
    main()    
         
        
        
    