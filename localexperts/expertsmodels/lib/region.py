'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''

class RegionBase:
    # contains tuples containing userid, user confidence, latitude , longitude, 
    # expertise (True if the user belongs the expertise of this region) in that order
    _usersData = [(77463542,0.98,67.9,-76.9,'aggie')]


class Region(RegionBase):
    _name = ''
    _leftTop = (0, 0)
    _rightBottom = (0, 0)
    _horizontalSize = 0
    _verticalSize = 0
    _center = (0,0)
    
    # Distinguishes a parent region
    _isParent = False
    
    #_parentRegion for a parentRegion will be None
    # All the regions which are formed after segmentation cannot be parent Regions
    _parentRegion = None
    
    
    
    # A row major matrix for the child regions resulting from segmentation 
    # of the parent region
    _childRegions = []
    
    def __init__(self, topLeft, rightBottom, name = 'New Region', isParent = False):
        self._isParent = isParent
        self._name = name
        self._rightBottom = rightBottom
        self._leftTop = topLeft
        self._calculateRegionAttributes()
        
    def _calculateRegionAttributes(self):
        # take the difference between longitude
        self._horizontalSize = abs(float(self._rightBottom[1] - self._leftTop[1]))
        # take the difference between latitude
        self._verticalSize = abs(float(self._rightBottom[0] - self._leftTop[0]))
        
        self._center = (self._leftTop[0] - self._verticalSize / 2, self._leftTop[1] + self._horizontalSize / 2)
    
    def boundsLocation(self, location):
        if location[0] >= self._rightBottom[0] and location[0] <= self._leftTop[0] :
            if location[1] <= self._rightBottom[1] and location[1] >= self._leftTop[1]:
                return True
        return False
    
    def getCenter(self):
        return self._center
    
    def getChildRegions(self):
        return self._childRegions
    
    def getChildRegion(self, horizontalIndex, verticalIndex):
        if len(self._childRegions) == 0:
            return None
        if horizontalIndex < len(self._childRegions[0]) and verticalIndex < len(self._childRegions):
            return self._childRegions[horizontalIndex][verticalIndex]
        return None
    
    @staticmethod
    def getUsersData():
        return RegionBase._usersData
    
    @staticmethod
    def addUserData(userData):
        RegionBase._usersData.append(userData)
        
    @staticmethod   
    def clearUsersData():
        RegionBase._usersData = []
        
    def getParent(self):
        return self._parentRegion
    
    def isParent(self):
        return self._isParent
    
    def setParentRegion(self, region):
        self._parentRegion = region
    
    def _segment(self, numHorizontalSegments, numVerticalSegments, childRegionHorizontalSize, childRegionVerticalSize):
        #print len(self._childRegions), 'is the number of children columns'
        self._childRegions = []
        #print 'segmenting ', self._name, ' into ', numHorizontalSegments,'x',numVerticalSegments,'segments'
        #print 'with horizontal size :',childRegionHorizontalSize,' with vertical size :', childRegionVerticalSize
        latitude = self._leftTop[0] 
        longitude = self._leftTop[1]
        # Segment regions and assign each of them with their 
        # lefttop and rightbottom
        for horizontalSegmentCount in range(numHorizontalSegments):
            horizontalChildRegions = []
            for verticalSegmentCount in range(numVerticalSegments):
                childTopLeft = (latitude - verticalSegmentCount * childRegionVerticalSize,
                                longitude + childRegionHorizontalSize * horizontalSegmentCount)
                childRightBottom = (latitude - (verticalSegmentCount + 1) * childRegionVerticalSize,
                                    longitude + childRegionHorizontalSize * (horizontalSegmentCount + 1))
                
                childRegionName = self._name + '\'s Child : '+ str(horizontalSegmentCount) + ',' + str(verticalSegmentCount)
                childRegion = Region(childTopLeft, childRightBottom, childRegionName, False)
                childRegion.setParentRegion(self)
                horizontalChildRegions.append(childRegion)
            self._childRegions.append(horizontalChildRegions)

    def segmentByChildCount(self, numHorizontalSegments, numVerticalSegments):
        childRegionHorizontalSize = self._horizontalSize / numHorizontalSegments
        childRegionVerticalSize = self._verticalSize / numVerticalSegments
        self._segment(numHorizontalSegments, numVerticalSegments, childRegionHorizontalSize, childRegionVerticalSize)
        
        
    '''
    Segments the region into the number of regions closest to the expected number of 
    regions.
    '''
    def segmentByChildSize(self, expectedChildRegionHorizontalSize , expectedChildRegionVerticalSize):
        if (expectedChildRegionHorizontalSize > 0 and expectedChildRegionVerticalSize > 0):
            numHorizontalSegments = int(round(self._horizontalSize / expectedChildRegionHorizontalSize)) 
            numVerticalSegments =  int(round(self._verticalSize / expectedChildRegionVerticalSize))
            
            residualVerticalSize = self._verticalSize - numVerticalSegments * expectedChildRegionVerticalSize
            residualHorizontalSize = self._horizontalSize - numHorizontalSegments * expectedChildRegionHorizontalSize
            
            # Calculating the actual size that each child region should have in order to cover the whole region
            childRegionVerticalSize = expectedChildRegionVerticalSize + residualVerticalSize / numVerticalSegments 
            childRegionHorizontalSize = expectedChildRegionHorizontalSize + residualHorizontalSize / numHorizontalSegments
            self._segment(numHorizontalSegments, numVerticalSegments, childRegionHorizontalSize, childRegionVerticalSize)
            

    def getName(self):
        return self._name
    
def main():
        print 'Testing Region Class'
        region = Region((57.93, -116.98), (43.2, -73.15), 'Test Region')
        print 'Region _center is ', region.getCenter()
        region.segmentByChildSize(5, 8)
        Region.addUserData((23,9,85,84,'aggie'))
        child = region.getChildRegion(0,0)
        child.segmentByChildSize(2,2)
        print 'Centres for the regions:'
        for children in child.getChildRegions():
            for childRegion in children:
                print childRegion._name,' center :', childRegion.getCenter(), 'leftTop: ', childRegion._leftTop, 'rightBottom: ', childRegion._rightBottom,'userdata: ', childRegion.getUsersData() 
    
if __name__ == "__main__":
    main()          
