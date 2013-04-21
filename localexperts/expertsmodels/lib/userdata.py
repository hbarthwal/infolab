'''
Created on Apr 16, 2013

@author: Himanshu Barthwal
'''
'''
The purpose of this class is to hold the userdata do some operations on them.
'''
from operator import itemgetter
from utility import Utility

class UsersData:
    # contains lists containing userid, user confidence, latitude , longitude, 
    # expertise (True if the user belongs the expertise of this region) in that order
    # e.g [77463542,0.98,67.9,-76.9,'aggie']
    _usersData = []
    
    _isPartitioned = False
    
    @staticmethod
    def isPartitioned():
        return UsersData._isPartitioned
    
    '''
    For every user belonging to the given expertise the value of confidence is computed
    using the multiple centre model and user is assigned to the model giving it the maximum 
    value of confidence.
    @param expertise: The expertise for which the models have been generated.
    @param expertModels: The models generated for the given expertise.
    '''
    @staticmethod
    def partitionUsers(expertModels, expertise):
        for userData in UsersData._usersData:
            pValues = []
            for expertModel in expertModels:
                p = Utility.getModelValue(expertModel, userData, userData[4] == expertise)
                pValues.append((p, expertModel['regionName']))
            maxPRegion = max(pValues, key = itemgetter(0))[1]
            if len(userData) == 5:
                userData.append(maxPRegion)
            else:
                userData[5] = maxPRegion
        UsersData._isPartitioned = True
    
    
    @staticmethod
    def addUserData(userData):
        UsersData._usersData.append(userData)
    
     
    @staticmethod
    def getUsersData():
        return UsersData._usersData
    
        
    @staticmethod   
    def clearUsersData():
        UsersData._usersData = []
    
    '''
    Adds the extracted user data to the expert regions 
    '''   
    @staticmethod 
    def addUserDataToRegions(usersDataForAllExpertise):
        # Add all the user data to the region
        _usersData = []
        print 'Adding all the user data to Region'
        for expertise in usersDataForAllExpertise:
            for userData in usersDataForAllExpertise[expertise]:
                UsersData.addUserData([userData[0], userData[1], userData[2], userData[3], userData[4]])
        print 'Added total ', len(UsersData.getUsersData()), ' entries to Region user data'
            
