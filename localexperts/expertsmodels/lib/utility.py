'''
Created on Apr 13, 2013

@author: himanshu
'''

from math import radians, cos, sin, asin, sqrt
from region import Region

class Utility:
    
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    @param longitudeCenter: The longitude of the center
    @param latitudeCenter:  The longitude of the center
    @param longitudeUser: The longitude of the user
    @param latitudeUser:  The longitude of the user
    
    @return: Haversine distance between the user and the center
    """
    @staticmethod
    def haversine(longitudeCenter, latitudeCenter, longitudeUser, latitudeUser):
        # convert decimal degrees to radians 
        longitudeCenter, latitudeCenter, longitudeUser, latitudeUser = map(radians, [longitudeCenter,
                                                                                     latitudeCenter,
                                                                                     longitudeUser,
                                                                                     latitudeUser])
        # haversine formula 
        diffLongitude = longitudeUser - longitudeCenter 
        diffLatitude = latitudeUser - latitudeCenter 
        a = sin(diffLatitude / 2) ** 2 + cos(latitudeCenter) * cos(latitudeUser) * sin(diffLongitude / 2) ** 2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km    
    
    '''
    Adds the extracted user data to the expert regions 
    '''   
    @staticmethod 
    def addUserDataToRegions(usersDataForAllExpertise):
        # Add all the user data to the region
        print 'Adding all the user data to Region'
        for expertise in usersDataForAllExpertise:
            for userData in usersDataForAllExpertise[expertise]:
                Region.addUserData((userData[0], userData[1], userData[2], userData[3], userData[4]))
        print 'Added total ', len(Region.getUsersData()), ' entries to Region user data'
