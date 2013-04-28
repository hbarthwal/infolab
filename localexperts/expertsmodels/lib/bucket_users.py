'''
Created on Apr 11, 2013

@author: Himanshu Barthwal
'''
from extractdata import DataExtractorFactory
from region import Region
from userdata import UsersData
from utility import Utility
import time
from pprint import pprint

class BucketUsers:
    
    _interval = 5
    
    _center = (0, 0)
    
    _expertCount = 0
    
    _usersData = None
    
    _region = None
    
    _bucketedUserData = {'5-10': {'averageDistance':3.5, 'confidenceSum': .786}}
    
    def __init__(self, region, interval):
        self._bucketedUserData.clear()
        self._region = region
        self._center = self._region.getCenter()
        self._interval = interval
        self._usersData = UsersData.getUsersData()
        self._bucketUserData()
        self._normalizeBuckets()
        
    '''
    Gets the bucket key for a user located at the given distance.
    @param distance: The distance at which the user is located
    @return: The corresponding key for the bucket in which the user will be 
             put in.
    '''
    def _getBucketKey(self, distance):
        index = int(distance / self._interval)
        bucketKey = str(self._interval * index) + '-' + str(self._interval * (index + 1))
        return bucketKey
    
    
    '''
    Bucket-wise averages the distances of all the expert and non-expert users 
    '''
    def _normalizeBuckets(self):
        # Now we average out all the users distances and confidences
        # within each bucket
        totalNonExpertCount = 0
        for bucketKey in self._bucketedUserData:
            usersBucket = self._bucketedUserData[bucketKey]
            
            expertUsersBucket = usersBucket['expert']
            expertUsersCount = float(expertUsersBucket['usersCount'])
            expertUsersDistanceSum = expertUsersBucket.pop('distanceSum')
            
            nonExpertUsersBucket = usersBucket['nonexpert']
            nonExpertUsersCount = float(nonExpertUsersBucket['usersCount'])            
            nonExpertUsersDistanceSum = nonExpertUsersBucket.pop('distanceSum')
            totalNonExpertCount += nonExpertUsersCount 
            if expertUsersCount != 0:
                expertUsersBucket['averageDistance'] = expertUsersDistanceSum / expertUsersCount
            else:
                expertUsersBucket.clear()
            
            if nonExpertUsersCount != 0:
                nonExpertUsersBucket['averageDistance'] = nonExpertUsersDistanceSum / nonExpertUsersCount 
            
            else:
                nonExpertUsersBucket.clear()
       
            # If no experts were found in the bucket clear the dictionary object
            if len(expertUsersBucket) == 0:
                usersBucket.pop('expert')
            
            # If no non-experts were found in the bucket clear the dictionary object
            if len(nonExpertUsersBucket) == 0:
                usersBucket.pop('nonexpert')
       
    '''
    Returns the pair of keys to be used.
    '''     
    def _getKeys(self, isExpert):
        requiredKey = ''
        nonRequiredKey = ''
        if isExpert:
            requiredKey = 'expert'
            nonRequiredKey = 'nonexpert'
        else:
            requiredKey = 'nonexpert'
            nonRequiredKey = 'expert'
        return requiredKey, nonRequiredKey

    '''
    Creates the buckets of expert and non expert users based on their 
    distance from the center of the region under consideration. All the
    users who are not in the root region of the current expertise
    will be ignored. 
    '''
    def _bucketUserData(self):
        #print 'Bucketing ', len(self._usersData), ' users !'
        #count = 0
        expertise = self._region.getExpertise()
        
        #print 'bucketing for ', self._region.getName()
        for userData in self._usersData:
            userLocation = (userData[2], userData[3])
            # print userData
            # The root expertise region from which this child has descended
            parentRegion = None
            if self._region.isParent():
                parentRegion = self._region
            else:
                parentRegion = self._region.getParent()
            
            
            if parentRegion.boundsLocation(userData):
                #count += 1
                # if the user data is corresponding to a location 
                # belonging to the expertise region only then we include it in
                # our calculation
                userConfidence = userData[1]
                userDistance = Utility.haversine(self._center[1], self._center[0], userLocation[1], userLocation[0])
                isExpert = (expertise == userData[4])
                distanceBucketKey = self._getBucketKey(userDistance)
                requiredKey, nonRequiredKey = self._getKeys(isExpert)
                
                if not distanceBucketKey in self._bucketedUserData:
                   
                    self._bucketedUserData[distanceBucketKey] = {}
                    self._bucketedUserData[distanceBucketKey][requiredKey] = {'distanceSum': userDistance,
                                                                      'confidenceSum': userConfidence,
                                                                      'usersCount': 1
                                                                     }
                    self._bucketedUserData[distanceBucketKey][nonRequiredKey] = {'distanceSum': 0.0,
                                                                              'confidenceSum': 0.0,
                                                                              'usersCount': 0
                                                                              }
                else:
                    # calculating the sum of all users' distance and confidence within a 
                    # certain radius denoted by the bucketKey
                    #print 'Incrementing------------------------------------'
                    self._bucketedUserData[distanceBucketKey][requiredKey]['distanceSum'] += userDistance
                    self._bucketedUserData[distanceBucketKey][requiredKey]['confidenceSum'] += userConfidence
                    self._bucketedUserData[distanceBucketKey][requiredKey]['usersCount'] += 1
        #print count,' users were bucketed'
    '''
    Returns the bucket dictionary for the users.
    '''    
    def getUsersBucket(self):
        return self._bucketedUserData
    
    
    '''
    For testing and debugging purposes.
    '''
    def printBuckets(self):
        totalExpertsCount = 0
        totalNonExpertsCount = 0
        for bucketKey in self._bucketedUserData:
            expertCount = 0
            expertConfindenceSum = 0 
            
            nonExpertCount = 0
            nonExpertConfindenceSum = 0 
            if 'expert' in self._bucketedUserData[bucketKey]:
                expertCount = self._bucketedUserData[bucketKey]['expert']['usersCount']
                expertConfindenceSum = self._bucketedUserData[bucketKey]['expert']['confidenceSum']
                totalExpertsCount += expertCount
                print 'Bucket ', bucketKey,' has ',expertCount, 'experts with expertConfindenceSum = ',expertConfindenceSum
                
            if 'nonexpert' in self._bucketedUserData[bucketKey]:
                nonExpertCount = self._bucketedUserData[bucketKey]['nonexpert']['usersCount']
                nonExpertConfindenceSum = self._bucketedUserData[bucketKey]['nonexpert']['confidenceSum']
                totalNonExpertsCount += nonExpertCount
                print 'Bucket ', bucketKey,' has ',nonExpertCount, 'nonexperts with expertConfindenceSum = ',nonExpertConfindenceSum
        
        print 'Total experts:', totalExpertsCount, ' Total non experts:', totalNonExpertsCount

def main():
    print 'Main'
    dataDirectory = 'data/'
    start = time.time()
    data = DataExtractorFactory.getDataExtractor('expertisemodel', dataDirectory)
    expertUsersData = data.getAllExpertsData()
    region = Region((50, -125), (25.255, -60),center = (30,-60) ,expertise='vc')
    UsersData.addUserDataToRegions(expertUsersData)
    usersBucket = BucketUsers(region, 50)
    print time.time() - start,' is the time taken'
    usersBucket.printBuckets()
    
    
if __name__ == "__main__":
    main()    
           
            
            
            
             
        
