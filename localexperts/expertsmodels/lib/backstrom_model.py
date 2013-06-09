'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
from math import log, pow
from multiprocessing import Process, Queue
from random import randint
from pprint import pprint
from operator import itemgetter
import time

from bucket_users import BucketUsers
from extractdata import DataExtractorFactory
from region import Region
from userdata import UsersData
#import map_plots 
from settings import Settings

class BackStromExpertiseModelGenerator:
    _dictExpertUsersData = {}
    _dictExpertiseRegions = {'tech': [Region((0, 0), (0, 0))]}
    _dictExpertModels = {'tech': [{'C':.8, 'alpha' : 2.9, 'center': (23, -67.9)}]}
    _dataDirectory = ''
    _expertDataExtractor = None
    _usersClusterer = None    
    _usersBucket = None
    
    def __init__(self, dataDirectory, dataExtractor = None):
        self._dictExpertiseRegions.clear()
        self._dictExpertModels.clear()
        self._dataDirectory = dataDirectory
        if dataExtractor == None:
            self._expertDataExtractor = DataExtractorFactory.getDataExtractor('expertisemodel', self._dataDirectory)
            self._expertDataExtractor.populateData(self._dataDirectory)
        else:
            self._expertDataExtractor = dataExtractor
            
        self._dictExpertUsersData = self._expertDataExtractor.getAllExpertsData()
        self._createParentRegions()
        UsersData.addUserDataToRegions(self._dictExpertUsersData)

    '''
    Calculates the likelihood value for Backstorm model p = C*d^-alpha
    @param C: The value of parameter C
    @param alpha: The value of parameter C
    @param childRegion: The childRegion for which we want to calculate the model
    '''
    def _likelihoodFunction(self, C, alpha, childRegion):
        expertValueSum = 0
        nonExpertValueSum = 0
        
        # We will use all the users data for a given expertise's parent childRegion
        # to calculate the log likelihood about the center of a 
        # given child childRegion.
        
        usersDataBuckets = self._usersBucket.getUsersBucket()
        if childRegion.getName() != self._usersBucket._region.getName():
            print childRegion.getName(), ' is using the bucket for ', self._usersBucket._region.getName()
        
        for bucketKey in usersDataBuckets:
            usersBucket = usersDataBuckets[bucketKey] 

            # We calculate the maximum likelihood for the Backstorm model
            # using the center of this childRegion as the center of the model
            expertModelValue, nonExpertModelValue = 0, 0
            
            if 'expert' in usersBucket:
                expertUsersBucket = usersBucket['expert'] 
                expertUsersConfidenceSum = expertUsersBucket['confidenceSum']
                expertUserDistance = expertUsersBucket['averageDistance']
                # expertUserCount = expertUsersBucket['usersCount']
                # try:
                if expertUserDistance <= 1:
                    expertUserDistance = 1.01
                expertModelValue = expertUsersConfidenceSum * log(C * pow(expertUserDistance, -alpha))
                # except:
                    # print 'Expert: distance->', expertUserDistance, ' confidence->' , expertUsersConfidenceSum
                    # print 'usersBucketKey', bucketKey
                    # raise
            
            if 'nonexpert' in usersBucket:    
                nonExpertUsersBucket = usersBucket['nonexpert']
                nonExpertUsersConfidenceSum = nonExpertUsersBucket['confidenceSum']
                nonExpertUserDistance = nonExpertUsersBucket['averageDistance']
                # nonExpertUserCount = nonExpertUsersBucket['usersCount']
                # try:
                if nonExpertUserDistance <= 1:
                    nonExpertUserDistance = 1.01
                nonExpertModelValue = (1 - C * pow(nonExpertUserDistance, -alpha))
                nonExpertModelValue = nonExpertUsersConfidenceSum * log(nonExpertModelValue)
            # except:
                    # print 'Non Expert: distance->', nonExpertUserDistance, ' confidence->' , nonExpertUsersConfidenceSum  
                    # print 'usersBucketKey', bucketKey
                    # raise
            #print 'Expert Value:', expertModelValue
            expertValueSum += expertModelValue
            nonExpertValueSum += nonExpertModelValue
        #print 'C = ', C, 'alpha = ', alpha
        #print 'Expert likelihood component:' , expertValueSum  
        #print 'non Expert likelihood component:' , nonExpertValueSum  
        functionValue = expertValueSum + nonExpertValueSum
        #print functionValue,' is the total likelihood value'
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
        aAlpha = Settings.alphaMin
        bAlpha = Settings.alphaMax
        
        while bAlpha - aAlpha > Settings.alphaTolerance:
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
        aC = Settings.Cmin
        bC = Settings.Cmax
        
        while bC - aC > Settings.Ctolerance:
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
        self._usersBucket = BucketUsers(region, Settings.bucketingInterval)
        # print 'prepared bucket for ', region.getName()
        # self._usersBucket.printBucket()
        value = self._goldenSectionSearch(region)
        return value
    
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
        # print 'calculating maximum likelihood for all regions in'+ parentRegion.getName() +' and getting the maximum parentRegion'
        previousMaxLikelihoodValue = maxLikelihoodValue = -9999999999999
        (argmaxC, argmaxAlpha) = (0, 0)
        mleRegion = None
        for childrenRegionRow in parentRegion.getChildRegions():
                for childRegion in childrenRegionRow:
                    (argmaxC, argmaxAlpha, value) = self._calculateMaxLogLikelihood(childRegion)
                    # print 'Got value =' , value
                    maxLikelihoodValue = max(maxLikelihoodValue, value)
                    # print 'Got mle Value = ', maxLikelihoodValue
                    if maxLikelihoodValue > previousMaxLikelihoodValue:
                        # print maxLikelihoodValue, ' is greater than ', previousMaxLikelihoodValue
                        mleRegion = childRegion
                        previousMaxLikelihoodValue = maxLikelihoodValue 
        return (mleRegion, argmaxC, argmaxAlpha)
    
    '''
    Calculates the Backstorm for a region and puts the calculted result into the queue.
    @param expertiseRegion: This is the region for which the backstorm model is calculated.
    @param queue: The queue in which the calculated model's data is pushed.
    '''
    def _computeModel(self, expertiseRegion, queue):
        region = expertiseRegion
        childRegionVerticalSize = Settings.initialChildRegionVerticalSize
        childRegionHorizontalSize = Settings.initialChildRegionHorizontalSize
        mleRegion = None
        print 'Computing model for', region.getName() 
        while childRegionHorizontalSize >= Settings.minChildRegionSize:
            region.segmentByChildSize(childRegionHorizontalSize, childRegionVerticalSize)
            mleRegion, argmaxC, argmaxAlpha = self._getMaximumLikelyChildRegion(region)
            # print mleRegion.getName(), ' has the largest mle value', 'C = ', argmaxC, ' alpha = ', argmaxAlpha
            region = mleRegion
            childRegionHorizontalSize = childRegionHorizontalSize / 2
            childRegionVerticalSize = childRegionVerticalSize / 2
        
        # Putting the resultant computed model into the queue
        dictResult = {'C':argmaxC,
                      'alpha':argmaxAlpha,
                      'center':mleRegion.getCenter(),
                      'regionName': expertiseRegion.getName()
		      }
        # print 'The resultant model is :', dictResult
        queue.put(dictResult)
    
    '''
    Spawn a subprocess for every region in the provided 'expertiseRegions' list
    and performs parallel computation then puts the results in to the provided 
    dataQueue asynchronously.
    @param expertiseRegions: A list of regions for which we want to compute the 
    backstorm model
    
    @param dataQueue: A queue which used by all the subprocess to store their results
    '''
    def _computeModelsParallely(self, expertiseRegions, dataQueue):
        processes = []
        for expertiseRegion in expertiseRegions:
            processName = expertiseRegion.getName() + 'process'
            process = Process(target=self._computeModel, args=(expertiseRegion, dataQueue), name=processName)
            processes.append(process)
        
        for process in processes:
            process.start()
        return processes
    
    '''
    The method reads the dataQueue and populates the '_dictExpertModels' dictionary
    with the results present in the dataQueue.
    @param expertise: The expertise for which the model data is residing in the dataQueue.
    @param dataQueue: The queue in which the model data is present
    '''
    def _populateResultsFromQueue(self, expertise, dataQueue):
    # All the children processes have finished their computation now
    # lets populate the dictionary with the results that they have
    # pushed into the queue.
        while not dataQueue.empty():
            modelDict = dataQueue.get()
            if expertise in self._dictExpertModels:
                # print 'Added Entry to dictionary for ', modelDict['regionName']
                self._dictExpertModels[expertise].append(modelDict)
            else:
                # print 'Appended entry for', modelDict['regionName']
                self._dictExpertModels[expertise] = [modelDict]
        
    '''
    Checks if all processes have finished computation if yes then returns 
    otherwise sleeps.
    '''
    def _waitForProcesses(self, processes):
    #  Here the current process sleeps while the subprocesses 
    #  are busy in computation
        while True:
            areAlive = False
            for process in processes:
                areAlive = areAlive or process.is_alive()
            if areAlive == False:
                break
            time.sleep(2)
    
    '''
    Simply a wrapper over _calculateMaxLogLikelihood to support
    multiprocessing.
    '''
    def _computeLogLikeliHood(self, expertiseRegion, dataQueue):
        (argmaxC, argmaxAlpha, maxLikelihoodValue) = self._calculateMaxLogLikelihood(expertiseRegion)
        # Putting the resultant computed model into the queue
        dictResult = {
                      'C':argmaxC,
                      'alpha':argmaxAlpha,
                      'center':expertiseRegion.getCenter(),
                      'regionName': expertiseRegion.getName()
                      }
        dataQueue.put(dictResult)
        
    '''
    Spawn a subprocess for every region in the provided 'expertiseRegions' list
    and performs parallel computation then puts the results in to the provided 
    dataQueue asynchronously.
    @param expertiseRegions: A list of regions for which we want to compute the 
    backstorm model
    
    @param dataQueue: A queue which used by all the subprocess to store their results
    '''
    def _computeLogLikelihoodValuesParallely(self, expertiseRegions, dataQueue):
        processes = []
        
        for expertiseRegion in expertiseRegions:
            processName = expertiseRegion.getName() + 'process'
            process = Process(target=self._computeLogLikeliHood, args=(expertiseRegion, dataQueue), name=processName)
            processes.append(process)
        
        for process in processes:
            process.start()
        
        self._waitForProcesses(processes)
        return processes
    
    def _optimizeParameters(self, expertise):
        expertiseRegions = self._dictExpertiseRegions[expertise]
        dataQueue = Queue(len(expertiseRegions))
        self._computeLogLikelihoodValuesParallely(expertiseRegions, dataQueue)
        self._populateResultsFromQueue(expertise, dataQueue)
    
    def _updateExpertiseRegions(self, expertise):
        dictRegionPartition = {}
        usersData = UsersData.getUsersData()
        for userData in usersData:
            regionName = userData[5]
            if regionName in dictRegionPartition:
                dictRegionPartition[regionName].append(userData)
            else:
                dictRegionPartition[regionName] = [userData]
            
        print 'Regions: ', dictRegionPartition.keys()
        dictCenters = {}
        for model in self._dictExpertModels[expertise]:
            dictCenters[model['regionName']] = model['center']
    
        expertRegions = []
        for regionName in dictRegionPartition:
            usersData = dictRegionPartition[regionName]
            print regionName, ' has ', len(usersData), ' users assigned to it out of', len(UsersData.getUsersData()), ' users'
            leftTop, rightBottom = self._getBoundingBox(usersData)
            try:
                expertRegion = Region(leftTop, rightBottom,
                                  center=dictCenters[regionName], name=regionName,
                                  isParent=True, expertise=expertise)
            
                expertRegions.append(expertRegion)
            except:
                print 'Region invalid.. discarded!!'
        self._dictExpertiseRegions[expertise] = expertRegions
        
                
    def _displayRegionsInfo(self, expertise):
        expertiseRegions = self._dictExpertiseRegions[expertise]
        models = self._dictExpertModels[expertise]
        #map_plots.plotRegion(expertiseRegions, models)
    
    '''
    Generates models for given expertises regions
    @param expertise: The expertise for which we want to generate Backstorm models.
    '''
    def generateModelForExpertise(self, expertise):
        print 'Generating model for', expertise
        # extracting the regions for the given expertise
        self._optimizeParameters(expertise)
        expertiseRegions = self._dictExpertiseRegions[expertise]
        dataQueue = Queue(len(expertiseRegions))
        print 'Initially computed models:-'
        pprint(self._dictExpertModels)
        iternum = 0
        while iternum < Settings.numberOfIterations:
            UsersData.partitionUsers(self._dictExpertModels[expertise], expertise)
            print 'Recomputed Bounding boxes for regions-----'
            self._updateExpertiseRegions(expertise)
            self._displayRegionsInfo(expertise)
            self._dictExpertModels.clear()
            expertiseRegions = self._dictExpertiseRegions[expertise]
            print '---- Recomputing the centers------------'
            start = time.time()
            processes = self._computeModelsParallely(expertiseRegions, dataQueue)
            self._waitForProcesses(processes)
            self._populateResultsFromQueue(expertise, dataQueue)
            print 'It took ', start - time.time(), ' seconds'
            print '---------------Generated multiple center model----------'
            pprint(self._dictExpertModels)
            iternum += 1 
    
    def generateSingleCenterModel(self, expertise):
        expertiseRegion = self._dictExpertiseRegions[expertise][0]
        dataQueue = Queue(1)
        self._computeModel(expertiseRegion, dataQueue)
        self._populateResultsFromQueue(expertise, dataQueue)
        self._dictExpertModels[expertise] = dataQueue.get()
        pprint(self._dictExpertModels)
            
    '''
    Generates models for all expertise extracted from the users data
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
        for expertise in self._dictExpertUsersData:
            self._initializeExpertRegions(expertise)
    
    '''
    Generates a random center for a given bounding region's lefttop and 
    right bottom coordinates
    
    @param leftTop: The coordinates tuple for the left top corner 
    of the region (latitude, longitude)
    @param rightBottom: The coordinates tuple for the right bottom 
    corner of the region (latitude, longitude)
    '''        
    def _getRandomCenter(self, leftTop, rightBottom):
        randomLattitude = randint(int(rightBottom[0] * 1000), int(leftTop[0] * 1000)) / 1000.0
        randomLongitude = randint(int(leftTop[1] * 1000), int(rightBottom[1] * 1000)) / 1000.0
        randomCenter = (randomLattitude, randomLongitude)
        return randomCenter
    
    '''
    Generates the random centers such that they are uniformly distributed over the 
    targeted geographical region
    '''
    
    def _getRandomCenters(self, leftTop, rightBottom):
        dummyRegion = Region(leftTop, rightBottom)
        childRegionCount = int(round(pow(Settings.numberOfcenters,0.5)))
        dummyRegion.segmentByChildCount(childRegionCount, childRegionCount)
        randomCenters = []
        for childRegionRow in dummyRegion.getChildRegions():
            for childRegion in childRegionRow:
                randomCenter = self._getRandomCenter(childRegion.getLeftTop(), childRegion.getRightBottom())
                randomCenters.append(randomCenter)
        return randomCenters
    '''
    Creates a bounding region for a certain expertise based on the
    location information in user data.
    @param expertise: The expertise for which we want to create a bounding
    region.
    @return: The bounding region corresponding to the expertise.
    '''
    def _getBoundingBox(self, expertUsersData):
        maxLatitude = max(expertUsersData, key=itemgetter(2))[2]
        minLatiude = min(expertUsersData, key=itemgetter(2))[2]
        maxLongitude = max(expertUsersData, key=itemgetter(3))[3]
        minLongitude = min(expertUsersData, key=itemgetter(3))[3]
        leftTop = maxLatitude, minLongitude
        rightBottom = minLatiude, maxLongitude
        return leftTop, rightBottom
    
    def _initializeExpertRegions(self, expertise):
        
        expertUsersData = self._dictExpertUsersData[expertise]
        if len(expertUsersData) == 0:
            return
        leftTop, rightBottom = self._getBoundingBox(expertUsersData)
        expertRegions = []
        centers = self._getRandomCenters(leftTop, rightBottom)
        for index in range(len(centers)):
                center = centers[index]
                regionName = str(expertise) + ' Region ' + str(index)
                expertRegion = Region(leftTop, rightBottom, center=center , name=regionName,
                              isParent=True, expertise=expertise)
                expertRegions.append(expertRegion)
          
        
        # print 'Coordinates : minlatitude = ', minLatiude, ', maxLatitude = ', maxLatitude
        # print 'minlongitude = ', minLongitude, ', maxlongitude = ', maxLongitude
        self._dictExpertiseRegions[expertise] = expertRegions
    
    '''
    Gets the expertise for a bounding region
    @param region: The expertise corresponding to the provided bounding Region.
    '''
    def _getExpertiseForRegion(self, region):
        return region.getName().split(' ')[0]
    
    def getModelsForExpertise(self, expertise):
        return self._dictExpertModels[expertise]
    
    def getModelsForAllExpertise(self):
        return self._dictExpertModels
    
    '''
    Methods for Debugging and testing purposes.
    '''
    def testGoldenSectionSearch(self, regionCenter, expertise):
        expertRegion = Region((45, -129), (25, -50),
                              center=regionCenter , name='Test Region',
                              isParent=True, expertise=expertise)
        self._usersBucket = BucketUsers(expertRegion, Settings.bucketingInterval)
        self._usersBucket.printBuckets()
        print self._goldenSectionSearch(expertRegion)
    
    def testLikelihood(self, regionCenter, expertise, C, alpha):
        expertRegion = Region((45, -129), (25, -50),
                              center=regionCenter , name='Test Region',
                              isParent=True, expertise=expertise)
        self._usersBucket = BucketUsers(expertRegion, Settings.bucketingInterval)
        print 'likelihood value:', self._likelihoodFunction(C, alpha, expertRegion)
        
    def display(self):
        print 'Models Created as follows'
        pprint(self._dictExpertModels)
    
def main():
    print 'Main'
    dataDirectory = 'expertisedata/'
    modelGenerator = BackStromExpertiseModelGenerator(dataDirectory)
    start = time.time()
    #print modelGenerator.testGoldenSectionSearch((33.174, -90.322), 'vc')
    #print modelGenerator.testLikelihood(regionCenter = (45.174, -126.322), expertise = 'vc', C = .9 , alpha = .5)
    #modelGenerator.generateSingleCenterModel('vc')
    modelGenerator.generateModelForAllExpertise()
    print 'Time Taken:', time.time() - start, ' seconds'
    modelGenerator.display()

if __name__ == "__main__":
    main()          
