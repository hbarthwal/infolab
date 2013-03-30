'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''

class Region:
    _name = ''
    _leftTop = (0, 0)
    _rightBottom = (0, 0)
    _horizontalSize = 0
    _verticalSize = 0
    _center = (0,0)
    # A row major matrix for the child regions resulting from segmentation 
    # of the parent region
    childRegions = []
    
    def __init__(self, topLeft, rightBottom, name = 'New Region'):
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
    
    def hasLocation(self, location):
        if location[0] <= self._rightBottom[0] and location[0] >= self._leftTop[0] :
            if location[1] <= self._rightBottom[1] and location[1] >= self._leftTop[1]:
                return True
        return False
    
    def getCenter(self):
        return self._center
    
    
    def getChildRegion(self, horizontalIndex, verticalIndex):
        if len(self.childRegions) == 0:
            return None
        
        if horizontalIndex < len(self.childRegions[0]) and verticalIndex < len(self.childRegions):
            return self.childRegions[horizontalIndex][verticalIndex]
        
        return None
    
    def segment(self, numHorizontalSegments, numVerticalSegments):
        childRegionHorizontalSize = self._horizontalSize / numHorizontalSegments
        childRegionVerticalSize = self._verticalSize / numVerticalSegments
        
        latitude = self._leftTop[0] 
        longitude = self._leftTop[1]
        
        for horizontalSegmentCount in range(numHorizontalSegments):
            horizontalChildRegions = []
            for verticalSegmentCount in range(numVerticalSegments):
                childTopLeft = (latitude - verticalSegmentCount * childRegionVerticalSize,
                                longitude + childRegionHorizontalSize * horizontalSegmentCount)
                childRightBottom = (latitude - (verticalSegmentCount + 1) * childRegionVerticalSize,
                                    longitude + childRegionHorizontalSize * (horizontalSegmentCount + 1))
                
                childRegionName = 'Child Region : '+ str(horizontalSegmentCount) + ',' + str(verticalSegmentCount)
                childRegion = Region(childTopLeft, childRightBottom, childRegionName)
                horizontalChildRegions.append(childRegion)
            self.childRegions.append(horizontalChildRegions)


def main():
        print 'Testing Region Class'
        region = Region((57.93, -116.98), (43.2, -73.15), 'Test Region')
        print 'Region _center is ', region.getCenter()
        print 'segmenting region into 5 x 5 regions'
        region.segment(5, 5)
        
        print 'Centres for the regions:'
        for i in range(5):
            for j in range(5):
                childRegion = region.getChildRegion(i, j)
                print childRegion._name,' _center :', childRegion.getCenter(), '_leftTop: ', childRegion._leftTop, '_rightBottom: ', childRegion._rightBottom 
        
    
if __name__ == "__main__":
    main()          
