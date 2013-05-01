'''
Created on Apr 13, 2013

@author: himanshu
'''

from math import radians, cos, sin, asin, sqrt

class Utility:
    
    '''
    Evaluates the user confidence based on the Backstorm model.
    '''
    @staticmethod
    def getModelValue(model, userLocation, isExpert):
        C = model['C']
        alpha = model['alpha']
        center = model['center']
        distance = Utility.haversine(center[0],center[1], userLocation[0], userLocation[1])
        value = C * pow(distance + 0.9, -alpha)
        if isExpert:
            return value
        else :
            return 1 - value
    
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
    
