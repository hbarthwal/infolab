'''
Created on Apr 11, 2013

@author: Himanshu Barthwal
'''
from extractdata import DataExtractor
from region import Region
from utility import Utility
from pprint import pprint

class BucketUsers:
    
    _interval = 5
    
    _center = (0, 0)
    
    _expertCount = 0
    
    _usersData = None
    
    _region = None
    #                   {radius: (approxDistance, averageConfidence)}
    _bucketedUserData = {5: {'averageDistance':3.5, 'confidenceSum': .786}}
    
    def __init__(self, region, interval):
        self._bucketedUserData.clear()
        self._region = region
        self._interval = interval
        self._usersData = Region.getUsersData()
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
        for bucketKey in self._bucketedUserData:
            usersBucket = self._bucketedUserData[bucketKey]
            
            expertUsersBucket = usersBucket['expert']
            expertUsersCount = float(expertUsersBucket.pop('usersCount'))
            expertUsersDistanceSum = expertUsersBucket.pop('distanceSum')
            
            nonExpertUsersBucket = usersBucket['nonexpert']
            nonExpertUsersCount = float(nonExpertUsersBucket.pop('usersCount'))            
            nonExpertUsersDistanceSum = nonExpertUsersBucket.pop('distanceSum')
             
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
        expertise = self._region.getExpertise()
        for userData in self._usersData:
            userLocation = (userData[2], userData[3])
            # print userData
            # The root expertise region from which this child has descended
            parentRegion = None
            if self._region.isParent():
                parentRegion = self._region
            else:
                parentRegion = self._region.getParent()
            
            
            if parentRegion.boundsLocation(userLocation):
                # if the user data is corresponding to a location 
                # belonging to the expertise region only then we include it in
                # our calculation
                userConfidence = userData[1]
                center = self._region.getCenter()
                userDistance = Utility.haversine(center[1], center[0], userLocation[1], userLocation[0])
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
                    self._bucketedUserData[distanceBucketKey][requiredKey]['distanceSum'] += userDistance
                    self._bucketedUserData[distanceBucketKey][requiredKey]['confidenceSum'] += userConfidence
                    self._bucketedUserData[distanceBucketKey][requiredKey]['usersCount'] += 1
        
    '''
    Returns the bucket dictionary for the users.
    '''    
    def getUsersBucket(self):
        return self._bucketedUserData


def main():
    print 'Main'
    dataDirectory = 'data/'
    data = DataExtractor(dataDirectory)
    expertUsersData = data.getAllExpertsData()
    region = Region((50, -129), (27, -61), expertise='aggie')
    Utility.addUserDataToRegions(expertUsersData)
    usersBucket = BucketUsers(region, 10)
    # pprint(usersBucket.getUsersBucket())
    
    
if __name__ == "__main__":
    main()    
           
            
            
            
             
        
