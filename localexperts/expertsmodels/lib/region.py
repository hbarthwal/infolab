'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
'''
This class is inherited by the Region class.
The purpose of this class is to hold the data inorder
to avoid the replication of the user data when we segment 
each region.
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
    _expertise = ''
    # Distinguishes a parent region
    _isParent = True
    
    #_parentRegion for a parentRegion will be None
    # All the regions which are formed after segmentation cannot be parent Regions
    _parentRegion = None
    
    # A row major matrix for the child regions resulting from segmentation 
    # of the parent region
    _childRegions = []
    
    '''
    Instantiates the object of the Region class
    @param topLeft: The tuple containing the latitude, longitude for the
    topleft point of the bounding region in that order.
    
    @param rightBottom:The tuple containing the latitude, longitude for the
    rightBottom point of the bounding region in that order.
    
    @param name: Optional argument which sets the name for the region.
    
    @param isParent: Indicates if this is the root region.
    '''
    def __init__(self, topLeft, rightBottom, 
                 name = 'New Region', 
                 isParent = True, 
                 expertise = 'Jacks Of All Trades'):
        
        self._isParent = isParent
        self._name = name
        self._rightBottom = rightBottom
        self._leftTop = topLeft
        self._expertise = expertise
        self._validateCoordinates()
        self._calculateRegionAttributes()
    
    '''
    Perform calculations for region attirbutes like horizontal size , 
    vertical size and center of the region.
    '''    
    def _calculateRegionAttributes(self):
        # take the difference between longitude
        self._horizontalSize = abs(float(self._rightBottom[1] - self._leftTop[1]))
        # take the difference between latitude
        self._verticalSize = abs(float(self._rightBottom[0] - self._leftTop[0]))
        
        self._center = (self._leftTop[0] - self._verticalSize / 2, self._leftTop[1] + self._horizontalSize / 2)
    
    def getExpertise(self):
        return self._expertise
    
    '''
    Checks if the given location is bounded by this region.
    @param location: The tuple containing the latitude and longitude of the 
    location in that order.
    @return: True if the given location is bounded by this region, False otherwise.
    '''
    def boundsLocation(self, location):
        if location[0] >= self._rightBottom[0] and location[0] <= self._leftTop[0] :
            if location[1] <= self._rightBottom[1] and location[1] >= self._leftTop[1]:
                return True
        return False
    
    '''
    Checks the provided bounding box coordinates makes sense, raises Runtime error
    if the coordinates are invalid
    '''
    def _validateCoordinates(self):
        if not (self._leftTop[0] >= self._rightBottom[0] and self._rightBottom[1] >= self._leftTop[1]):
            raise RuntimeError('Invalid bounding region !!')
   
    '''
    Gets the location of the center.
    @return : A tuple  containing the latitude and longitude of the 
    center in that order.
    '''
    def getCenter(self):
        return self._center
    
    '''
    Gets the childRegions of the region.
    @return : A list of list of horizontal child regions of the region.
    '''
    def getChildRegions(self):
        return self._childRegions
    
    '''
    Gets the child region located at the given indices.
    
    @param horizontalIndex: The column index of the child
    @param verticalIndex: The row index of the child
    '''
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
        
    '''
    Gets the parent or the root region for this region.
    @return: The parent Region.
    '''
    def getParent(self):
        return self._parentRegion
    
    '''
    Checks if this region is a parent.
    @return : True if this region is a parent, False otherwise.
    '''
    def isParent(self):
        return self._isParent
    
    '''
    Sets the parent of the given region.
    @param region: The parent Region.
    '''
    def setParentRegion(self, region):
        self._isParent= False
        self._parentRegion = region
    
    '''
    Segments this region in to given number of child Regions of given size.
    @param numHorizontalSegments: Number of horizontal segments
    @param numVerticalSegments: Number of horizontal segments
    @param childRegionHorizontalSize : The horizontal size of each child
    @param childRegionVerticalSize : The vertical size of each child
    '''
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
                
                childRegionName = self._name + '\'s Child : '+ str(verticalSegmentCount) + ',' + str(horizontalSegmentCount)
                childRegion = Region(childTopLeft, childRightBottom, childRegionName, False, self.getExpertise())
                
                if self._parentRegion == None:
                    childRegion.setParentRegion(self)
                else:
                    childRegion.setParentRegion(self.getParent())
                horizontalChildRegions.append(childRegion)
            self._childRegions.append(horizontalChildRegions)

    '''
    Segments this region in to given number of child Regions.
    @param numHorizontalSegments: Number of horizontal segments
    @param numVerticalSegments: Number of horizontal segments
    '''
    def segmentByChildCount(self, numHorizontalSegments, numVerticalSegments):
        childRegionHorizontalSize = self._horizontalSize / numHorizontalSegments
        childRegionVerticalSize = self._verticalSize / numVerticalSegments
        self._segment(numHorizontalSegments, numVerticalSegments, childRegionHorizontalSize, childRegionVerticalSize)
        
    '''
    Segments the region into the number of regions closest to the expected size of 
    regions.
    @param expectedChildRegionHorizontalSize : The expected horizontal size of each child
    @param expectedChildRegionVerticalSize : The expected vertical size of each child
    '''
    def segmentByChildSize(self, expectedChildRegionHorizontalSize , expectedChildRegionVerticalSize):
        if (expectedChildRegionHorizontalSize > 0 and expectedChildRegionVerticalSize > 0):
            numHorizontalSegments = int(round(self._horizontalSize / expectedChildRegionHorizontalSize)) 
            numVerticalSegments =  int(round(self._verticalSize / expectedChildRegionVerticalSize))
            
            if numHorizontalSegments == 0 or numVerticalSegments == 0:
                self._childRegions = []
                self._childRegions.append([self])
                return
                
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
