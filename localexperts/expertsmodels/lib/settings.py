'''
Created on Apr 23, 2013

@author: himanshu
'''

class Settings:
    '''
      BackStrom Model Settings 
    '''
    _numberOfIterations = 10
    
    _numberOfcenters = 10
    _bucketingInterval = 40
    
    # min - max values for the C and alpha parameter 
    _alphaMin = 0.01
    _alphaMax = 9.99
    _Cmin = 0.001
    _Cmax = 0.999
    # tolerance values for the golden section search algorithm
    _Ctolerance = .001
    _alphaTolerance = 0.01
    
    # intial size of each grid
    _initialChildRegionVerticalSize = 2
    _initialChildRegionHorizontalSize = 2
    # minimum size of grid
    _minChildRegionSize = .1
    

    '''
     Data extractor settings
    '''   
    _maxExperts = 5000
    _dataFileNamePartOne = 'expert_locations_for_'
    _dataFileNamePartTwo = '_full_data.txt'
    _filterList = [
                      { 
                       'leftTopCoordinates' : (50, -125),
                       'rightBottomCoordinates' : (25.255, -60),
                       'region' : 'USA'
                      }
                   ]