'''
Created on Apr 23, 2013

@author: himanshu
'''

class Settings:
    '''
      BackStrom Model Settings 
    '''
    numberOfIterations = 10
    
    numberOfcenters = 10
    bucketingInterval = 40
    
    # min - max values for the C and alpha parameter 
    alphaMin = 0.01
    alphaMax = 9.99
    Cmin = 0.001
    Cmax = 0.999
    # tolerance values for the golden section search algorithm
    Ctolerance = .001
    alphaTolerance = 0.01
    
    # intial size of each grid
    initialChildRegionVerticalSize = 2
    initialChildRegionHorizontalSize = 2
    # minimum size of grid
    minChildRegionSize = .1
    

    '''
     Data extractor settings
    '''   
    maxExperts = 5000
    dataFileNamePartOne = 'expert_locations_for_'
    dataFileNamePartTwo = '_full_data.txt'
    filterList = [
                      { 
                       'leftTopCoordinates' : (50, -129),
                       'rightBottomCoordinates' : (25.255, -60),
                       'region' : 'USA'
                      }
                   ]
    userDataFileName = 'list_creator_user_location.json'
    expertUserListFileName = 'userids.txt'