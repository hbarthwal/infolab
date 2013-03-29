'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''

class Region:
    name = ''
    leftTop = (0, 0)
    rightBottom = (0, 0)
    horizontalSize = 0
    verticalSize = 0
    center = (0,0)
    # A row major matrix for the child regions resulting from segmentation 
    # of the parent region
    childRegions = []
    
    def __init__(self, topLeft, rightBottom, name = 'New Region'):
        self.name = name
        self.rightBottom = rightBottom
        self.leftTop = topLeft
        self._calculateRegionAttributes()
        
    def _calculateRegionAttributes(self):
        # take the difference between longitude
        self.horizontalSize = abs(float(self.rightBottom[1] - self.leftTop[1]))
        # take the difference between latitude
        self.verticalSize = abs(float(self.rightBottom[0] - self.leftTop[0]))
        
        self.center = (self.leftTop[0] - self.verticalSize / 2, self.leftTop[1] + self.horizontalSize / 2)
    
    def hasLocation(self, location):
        if location[0] <= self.rightBottom[0] and location[0] >= self.leftTop[0] :
            if location[1] <= self.rightBottom[1] and location[1] >= self.leftTop[1]:
                return True
        return False
    
    def getCenter(self):
        return self.center
    
    
    def getChildRegion(self, horizontalIndex, verticalIndex):
        if len(self.childRegions) == 0:
            return None
        
        if horizontalIndex < len(self.childRegions[0]) and verticalIndex < len(self.childRegions):
            return self.childRegions[horizontalIndex][verticalIndex]
        
        return None
    
    def segment(self, numHorizontalSegments, numVerticalSegments):
        childRegionHorizontalSize = self.horizontalSize / numHorizontalSegments
        childRegionVerticalSize = self.verticalSize / numVerticalSegments
        
        latitude = self.leftTop[0] 
        longitude = self.leftTop[1]
        
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
        print 'Region center is ', region.getCenter()
        print 'segmenting region into 5 x 5 regions'
        region.segment(5, 5)
        
        print 'Centres for the regions:'
        for i in range(5):
            for j in range(5):
                childRegion = region.getChildRegion(i, j)
                print childRegion.name,' center :', childRegion.getCenter(), 'leftTop: ', childRegion.leftTop, 'rightBottom: ', childRegion.rightBottom 
        
    
if __name__ == "__main__":
    main()          
