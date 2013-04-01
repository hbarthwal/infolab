'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
from region import Region
from extractdata import DataExtractor
from math import radians, cos, sin, asin, sqrt, log, pow
from operator import itemgetter
from pprint import pprint

class BackStormModelGenerator:
    _dictExpertUsersData = {}
    _dictExpertiseRegions = {'tech': [Region((0, 0), (0, 0))]}
    _dictExpertModels = {'tech': [{'C':.8, 'alpha' : 2.9, 'center': (23, -67.9)}]}
    _dataDirectory = ''
    _dataExtractor = None
    
    # min - max values for the C and alpha parameter 
    _alphaMin = 0.01
    _alphaMax = 10
    _Cmin = 0.01
    _Cmax = 0.99
    # tolerance values for the golden section search algorithm
    _Ctolerance = .01
    _alphaTolerance = 0.1
    
    # intial size of each grid
    _initialChildRegionVerticalSize = 10
    _initialChildRegionHorizontalSize = 10
    # minimum size of grid
    _minChildRegionSize = .5
    
    def __init__(self, dataDirectory):
        self._dictExpertiseRegions.clear()
        self._dictExpertModels.clear()
        self._dataDirectory = dataDirectory
        self._dataExtractor = DataExtractor(self._dataDirectory)
        self._dataExtractor.populateData(self._dataDirectory)
        self._createParentRegions()
        self._addUserDataToRegions()

    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    @param longitudeCenter: The longitude of the center
    @param latitudeCenter:  The longitude of the center
    @param longitudeUser: The longitude of the user
    @param latitudeUser:  The longitude of the user
    
    @return: Haversine distance between the user and the center
    """
    def _haversine(self, longitudeCenter, latitudeCenter, longitudeUser, latitudeUser):
        # convert decimal degrees to radians 
        longitudeCenter, latitudeCenter, longitudeUser, latitudeUser = map(radians, [longitudeCenter, latitudeCenter, longitudeUser, latitudeUser])
        # haversine formula 
        diffLongitude = longitudeUser - longitudeCenter 
        diffLatitude = latitudeUser - latitudeCenter 
        a = sin(diffLatitude / 2) ** 2 + cos(latitudeCenter) * cos(latitudeUser) * sin(diffLongitude / 2) ** 2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km    

    '''
    Calculates the likelihood value for Backstorm model p = C*d^-alpha
    @param C: The value of parameter C
    @param alpha: The value of parameter C
    @param childRegion: The childRegion for which we want to calculate the model
    '''
    def _likelihoodFunction(self, C, alpha, childRegion):
        
        expertValue = 0
        nonExpertValue = 0
        
        # the field of expertise to which is child region belongs
        expertise = self._getExpertiseForRegion(childRegion)
        
        # the root region from which this child has descended 
        parentRegion = self._dictExpertiseRegions[expertise][0]
       
        # We will use all the users location for a given expertise's parent childRegion
        # to calculate the log likelihood about the center of a 
        # given child childRegion.
        expertUsersData = Region.getUsersData()
        for userData in expertUsersData:
            
            location = (latitude, longitude) = (userData[2], userData[3])
            # if the user data is corresponding to a location 
            # belonging to the expertise region only then we include it in
            # our calculation
            if parentRegion.boundsLocation(location):
                 
                # We calculate the maximum likelihood for the Backstorm model
                # using the center of this childRegion as the center of the model
                center = childRegion.getCenter()
                distance = self._haversine(center[1], center[0], longitude, latitude)
                modelValue = C * pow(distance, -alpha)
                # if user is an expert in the expertise of the given childRegion
                if userData[4] == expertise:
                    expertValue += log(modelValue)
                else:
                    # if user is not an expert in the expertise of the given childRegion
                    nonExpertValue += log(1 - modelValue)
        
        functionValue = expertValue + nonExpertValue
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
            #print 'bAlpha:',bAlpha,' ','aAlpha:',aAlpha,' '
            x1Alpha = aAlpha + (1 - goldenRatio) * (bAlpha - aAlpha)
            x2Alpha = aAlpha + goldenRatio * (bAlpha - aAlpha)
            #print 'x1Alpha:',x1Alpha,' ','x2Alpha:',x2Alpha
           
            fx1Alpha = self._likelihoodFunction(C, x1Alpha, childRegion)
            fx2Alpha = self._likelihoodFunction(C, x2Alpha, childRegion)
            
            if fx1Alpha >= fx2Alpha:
                bAlpha = x2Alpha
            else:
                aAlpha = x1Alpha
        
        argmaxAlpha = (aAlpha + bAlpha) / 2
        maxLikelihoodValue = self._likelihoodFunction(C, argmaxAlpha, childRegion)
        #print 'argmaxAlpha : ',argmaxAlpha,'maxlikelihoodValue :', maxLikelihoodValue
        return (argmaxAlpha, maxLikelihoodValue)

    '''
    Calculates the alpha for maximum value of likelihood function for 
    childRegion and returns the tuple (C, alpha, maxLikelihoodValue)
    @param C: The value of parameter C
    @param childRegion: The childRegion for which we want to calculate the model
    '''
    def _goldenSectionSearch(self, childRegion):
        print '-----------------'
        # Golden section search for C and alpha parameters  
        goldenRatio = 0.618
        aC = self._Cmin
        bC = self._Cmax
        
        while bC - aC > self._Ctolerance:
            #print 'aC:',aC,' ','bC:',bC,' '
            x1C = aC + (1 - goldenRatio) * (bC - aC)
            x2C = aC + goldenRatio * (bC - aC)
            #print 'x1C:',x1C,' ','x2C:',x2C
            
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
        print 'calculating the log likelihood value for region', region.getName()
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
        print 'calculating maximum likelihood for all regions in'+ parentRegion.getName() +' and getting the maximum parentRegion'
        previousMaxLikelihoodValue = maxLikelihoodValue = -9999999999999
        (argmaxC, argmaxAlpha) = (0, 0)
        mleRegion = parentRegion.getChildRegion(0, 0)
        for childrenRegionRow in parentRegion.getChildRegions():
                for childRegion in childrenRegionRow:
                    (argmaxC, argmaxAlpha, value) = self._calculateMaxLogLikelihood(childRegion)
                    print 'Got value =' , value
                    maxLikelihoodValue = max(maxLikelihoodValue, value)
                    print 'Got mle Value = ', maxLikelihoodValue
                    if maxLikelihoodValue > previousMaxLikelihoodValue:
                        print maxLikelihoodValue, ' is greater than ', previousMaxLikelihoodValue
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
            print region.getName(),' has lefttop :', region._leftTop, ' rightbottom :',region._rightBottom  
            while childRegionHorizontalSize >= self._minChildRegionSize:
                region.segmentByChildSize(childRegionHorizontalSize, childRegionVerticalSize)
                (mleRegion, argmaxC, argmaxAlpha) = self._getMaximumLikelyChildRegion(region)
                print mleRegion.getName(), ' has the largest mle value','C = ', argmaxC, ' alpha = ', argmaxAlpha 
                region = mleRegion
                childRegionHorizontalSize = childRegionHorizontalSize / 2
                childRegionVerticalSize = childRegionVerticalSize / 2
        
        if expertise in self._dictExpertModels:
            self._dictExpertModels[expertise].append({'C':argmaxC, 'alpha': argmaxAlpha, 'center': mleRegion.getCenter()})
        else:
            self._dictExpertModels[expertise] = [{'C':argmaxC, 'alpha': argmaxAlpha, 'center': mleRegion.getCenter()}]
    
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
        expertRegion = Region(leftTop, rightBottom, expertise + ' Region', True)
        print 'Coordinates : minlatitude = ', minLatiude, ', maxLatitude = ', maxLatitude
        print 'minlongitude = ', minLongitude, ', maxlongitude = ', maxLongitude
        return expertRegion
        
    '''
    Adds the extracted user data to the expert regions 
    '''    
    def _addUserDataToRegions(self):
        usersDataForAllExpertise = self._dictExpertUsersData
        # Add all the user data to the region
        print 'Adding all the user data to Region'
        for expertise in usersDataForAllExpertise:
            for userData in usersDataForAllExpertise[expertise]:
                Region.addUserData((userData[0], userData[1], userData[2], userData[3], expertise))
        print 'Added total ', len(Region.getUsersData()), ' entries to Region user data'
    
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
    dataDirectory = '/home/himanshu/workspace/infolab/localexperts/expertsmodels/lib/data/expert_locations'
    modelGenerator = BackStormModelGenerator(dataDirectory)
    modelGenerator.generateModelForAllExpertise()
    modelGenerator.display()


if __name__ == "__main__":
    main()          
