'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
from region import Region
from extractdata import DataExtractor
from math import log, pow
from bucket_users import BucketUsers
from operator import itemgetter
from utility import Utility
from pprint import pprint

class BackStormModelGenerator:
    _dictExpertUsersData = {}
    _dictExpertiseRegions = {'tech': [Region((0, 0), (0, 0))]}
    _dictExpertModels = {'tech': [{'C':.8, 'alpha' : 2.9, 'center': (23, -67.9)}]}
    _dataDirectory = ''
    _dataExtractor = None
    
    _usersBucket = None
    _bucketingInterval = 20 
    # min - max values for the C and alpha parameter 
    _alphaMin = 0.001
    _alphaMax = 9.99
    _Cmin = 0.001
    _Cmax = 0.999
    # tolerance values for the golden section search algorithm
    _Ctolerance = .01
    _alphaTolerance = 0.001
    
    # intial size of each grid
    _initialChildRegionVerticalSize = 2
    _initialChildRegionHorizontalSize = 2
    # minimum size of grid
    _minChildRegionSize = .01
    
    def __init__(self, dataDirectory):
        self._dictExpertiseRegions.clear()
        self._dictExpertModels.clear()
        self._dataDirectory = dataDirectory
        self._dataExtractor = DataExtractor(self._dataDirectory)
        self._dataExtractor.populateData(self._dataDirectory)
        self._createParentRegions()
        Utility.addUserDataToRegions(self._dictExpertUsersData)


    '''
    Calculates the likelihood value for Backstorm model p = C*d^-alpha
    @param C: The value of parameter C
    @param alpha: The value of parameter C
    @param childRegion: The childRegion for which we want to calculate the model
    '''
    def _likelihoodFunction(self, C, alpha, childRegion):
        
        expertValueSum = 0
        nonExpertValueSum = 0
        
        # We will use all the users location for a given expertise's parent childRegion
        # to calculate the log likelihood about the center of a 
        # given child childRegion.
        
        usersDataBuckets = self._usersBucket.getUsersBucket()
        expertCount = 0
        for bucketKey in usersDataBuckets:
            
            usersBucket = usersDataBuckets[bucketKey] 
            
            # We calculate the maximum likelihood for the Backstorm model
            # using the center of this childRegion as the center of the model
            expertModelValue, nonExpertModelValue = 0, 0
            
            if 'expert' in usersBucket:
                expertUsersBucket = usersBucket['expert'] 
                expertUsersConfidenceSum = expertUsersBucket['confidenceSum']
                expertUserDistance = expertUsersBucket['averageDistance']
                try:
                    if expertUserDistance == 0:
                        expertUserDistance = 0.01
                    expertModelValue = C * pow(expertUserDistance, -alpha)
                    expertModelValue = expertUsersConfidenceSum * log(expertModelValue)
                    expertCount += 1
                except:
                    print 'Expert: distance->',expertUserDistance,' confidence->' ,expertUsersConfidenceSum
                    print 'usersBucketKey', bucketKey
                    raise
            
            elif 'nonexpert' in usersBucket:    
                nonExpertUsersBucket = usersBucket['nonexpert']
                nonExpertUsersConfidenceSum = nonExpertUsersBucket['confidenceSum']
                nonExpertUserDistance = nonExpertUsersBucket['averageDistance']
                try:
                    if nonExpertUserDistance == 0:
                        nonExpertUserDistance = 0.01
                    nonExpertModelValue = C * pow(nonExpertUserDistance, -alpha)
                    if nonExpertModelValue >= 1:
                        nonExpertModelValue = .99
                    nonExpertModelValue = nonExpertUsersConfidenceSum * log(1 - nonExpertModelValue)
                except:
                    print 'Non Expert: distance->', nonExpertUserDistance,' confidence->' ,nonExpertUsersConfidenceSum  
                    print 'usersBucketKey', bucketKey
                    raise
            
            expertValueSum += expertModelValue
            nonExpertValueSum += nonExpertModelValue
            
        functionValue = expertValueSum + nonExpertValueSum
        return functionValue
      
    '''
    Calculates the alpha for maximum value of likelihood function for 
    childRegion for a fixed value of C
    @param C: The value of parameter C
    @param childRegion: The childRegion for which we want to calculate the model
    '''      
    def _goldenSectionSearchForAlpha(self, C, childRegion):
        # Golden section search for alpha parameter for a fixed C
        goldenRatio = 0.618
        aAlpha = self._alphaMin
        bAlpha = self._alphaMax
        
        while bAlpha - aAlpha > self._alphaTolerance:
            x1Alpha = aAlpha + (1 - goldenRatio) * (bAlpha - aAlpha)
            x2Alpha = aAlpha + goldenRatio * (bAlpha - aAlpha)
           
            fx1Alpha = self._likelihoodFunction(C, x1Alpha, childRegion)
            fx2Alpha = self._likelihoodFunction(C, x2Alpha, childRegion)
            
            if fx1Alpha >= fx2Alpha:
                bAlpha = x2Alpha
            else:
                aAlpha = x1Alpha
        
        argmaxAlpha = (aAlpha + bAlpha) / 2
        maxLikelihoodValue = self._likelihoodFunction(C, argmaxAlpha, childRegion)
        return (argmaxAlpha, maxLikelihoodValue)

    '''
    Calculates the alpha for maximum value of likelihood function for 
    childRegion and returns the tuple (C, alpha, maxLikelihoodValue)
    @param C: The value of parameter C
    @param childRegion: The childRegion for which we want to calculate the model
    '''
    def _goldenSectionSearch(self, childRegion):
        # Golden section search for C and alpha parameters  
        goldenRatio = 0.618
        aC = self._Cmin
        bC = self._Cmax
        
        while bC - aC > self._Ctolerance:
            x1C = aC + (1 - goldenRatio) * (bC - aC)
            x2C = aC + goldenRatio * (bC - aC)
            
            fx1C = self._goldenSectionSearchForAlpha(x1C, childRegion)[1]
            fx2C = self._goldenSectionSearchForAlpha(x2C, childRegion)[1]
            
            if fx1C >= fx2C:
                bC = x2C
            else:
                aC = x1C
                
        argmaxC = (aC + bC) / 2
        (argmaxAlpha, maxLikelihoodValue) = self._goldenSectionSearchForAlpha(argmaxC, childRegion)
        return (argmaxC, argmaxAlpha, maxLikelihoodValue)
    
    '''
    Just a wrapper method which hides how exactly the maximum likehood value is 
    calculated.
    '''
    def _calculateMaxLogLikelihood(self, region):
        #print 'calculating the log likelihood value for region', region.getName()
        self._usersBucket = BucketUsers(region, self._bucketingInterval)
        return self._goldenSectionSearch(region)
   
    '''
    Finds the childRegion of the given parentRegion for which it 
    is maximum likely that the center of the Backstorm model will 
    lie in the center of this childRegion. This method calculates the 
    likelihood values for  all the children region then return the one 
    with maximum likelihood value.
    
    @param parentRegion: The parent region.
    @return : A tuple containing the mleRegion, argmaxC, argmaxAlpha in that order.
    mleRegion : The maximum likely region.
    argmaxC : The value of C which maximizes the likelihood function for the given 
    mleRegion.
    argmaxAlpha: The value of alpha which maximizes the likelihood function for the given 
    mleRegion.
    '''
    def _getMaximumLikelyChildRegion(self, parentRegion):
        #print 'calculating maximum likelihood for all regions in'+ parentRegion.getName() +' and getting the maximum parentRegion'
        previousMaxLikelihoodValue = maxLikelihoodValue = -9999999999999
        (argmaxC, argmaxAlpha) = (0, 0)
        mleRegion = parentRegion.getChildRegion(0, 0)
        for childrenRegionRow in parentRegion.getChildRegions():
                for childRegion in childrenRegionRow:
                    (argmaxC, argmaxAlpha, value) = self._calculateMaxLogLikelihood(childRegion)
                    #print 'Got value =' , value
                    maxLikelihoodValue = max(maxLikelihoodValue, value)
                    #print 'Got mle Value = ', maxLikelihoodValue
                    if maxLikelihoodValue > previousMaxLikelihoodValue:
                        #print maxLikelihoodValue, ' is greater than ', previousMaxLikelihoodValue
                        mleRegion = childRegion
                        previousMaxLikelihoodValue = maxLikelihoodValue 
        return (mleRegion, argmaxC, argmaxAlpha)
    
    '''
    Generates models for given expertise
    @param expertise: The expertise for which we want to generate Backstorm model.
    '''
    def generateModelForExpertise(self, expertise):
        print 'Generating model for', expertise
        childRegionVerticalSize = self._initialChildRegionVerticalSize
        childRegionHorizontalSize = self._initialChildRegionHorizontalSize
        # extracting the region for the given expertise
        expertiseRegions = self._dictExpertiseRegions[expertise]
        for expertiseRegion in expertiseRegions:
            region = expertiseRegion
            #print region.getName(),' has lefttop :', region._leftTop, ' rightbottom :',region._rightBottom  
            while childRegionHorizontalSize >= self._minChildRegionSize:
                region.segmentByChildSize(childRegionHorizontalSize, childRegionVerticalSize)
                (mleRegion, argmaxC, argmaxAlpha) = self._getMaximumLikelyChildRegion(region)
                #print mleRegion.getName(), ' has the largest mle value','C = ', argmaxC, ' alpha = ', argmaxAlpha 
                region = mleRegion
                childRegionHorizontalSize = childRegionHorizontalSize / 2
                childRegionVerticalSize = childRegionVerticalSize / 2
        
        if expertise in self._dictExpertModels:
            self._dictExpertModels[expertise].append({'C':argmaxC, 'alpha': argmaxAlpha, 'center': mleRegion.getCenter()})
        else:
            self._dictExpertModels[expertise] = [{'C':argmaxC, 'alpha': argmaxAlpha, 'center': mleRegion.getCenter()}]
        
        pprint(self._dictExpertModels[expertise]) 
    
    '''
    Generates models for all expertise extracted from the usersdata
    '''
    def generateModelForAllExpertise(self):
        print 'Generating model for all expertise'
        for expertise in self._dictExpertiseRegions:
            self.generateModelForExpertise(expertise)
    
    '''
    Creates bounding regions for all the expertise extracted from the users data
    '''
    def _createParentRegions(self):
        print 'creating parent Regions'
        print 'For now we only create one region per expertise'
        self._dictExpertUsersData = self._dataExtractor.getAllExpertsData()
        for expertise in self._dictExpertUsersData:
            expertiseRegion = self._createParentRegion(expertise)
            self._dictExpertiseRegions[expertise] = [expertiseRegion]
    
    '''
    Creates a bounding region for a certain expertise based on the
    location information in user data.
    @param expertise: The expertise for which we want to create a bounding
    region.
    @return: The bounding region corresponding to the expertise.
    '''
    def _createParentRegion(self, expertise):
        print 'Creating region for ', expertise 
        usersDataForAllExpertise = self._dictExpertUsersData
        expertUsersData = usersDataForAllExpertise[expertise]
        maxLatitude = max(expertUsersData, key=itemgetter(2))[2]
        minLatiude = min(expertUsersData, key=itemgetter(2))[2]
        maxLongitude = max(expertUsersData, key=itemgetter(3))[3]
        minLongitude = min(expertUsersData, key=itemgetter(3))[3]
        leftTop = (maxLatitude, minLongitude)
        rightBottom = (minLatiude, maxLongitude)
        expertRegion = Region(leftTop, rightBottom, expertise + ' Region', True, expertise = expertise)
        print 'Coordinates : minlatitude = ', minLatiude, ', maxLatitude = ', maxLatitude
        print 'minlongitude = ', minLongitude, ', maxlongitude = ', maxLongitude
        return expertRegion
        
    
    '''
    Gets the expertise for a bounding region
    @param region: The expertise corresponding to the provided bounding Region.
    '''
    def _getExpertiseForRegion(self, region):
        return region.getName().split(' ')[0]
    
    def display(self):
        print 'Models Created as follows'
        pprint(self._dictExpertModels)
    
def main():
    print 'Main'   
    dataDirectory = 'data/'
    modelGenerator = BackStormModelGenerator(dataDirectory)
    #modelGenerator.generateModelForExpertise('aggie')
    modelGenerator.generateModelForExpertise('rap')
    modelGenerator.generateModelForExpertise('vc')
    #modelGenerator.generateModelForExpertise('longhorn')
    modelGenerator.display()


if __name__ == "__main__":
    main()          
