'''
Created on Apr 13, 2013

@author: Himanshu Barthwal
'''
from operator import itemgetter
from region import Region
from extractdata import DataExtractorFactory
from sklearn.cluster import KMeans
from numpy import asarray, empty, float


class UsersClustering:
    
    _dictExpertUsersData = {'aggie':[(1445345,.6678, 45,-63)]}
    _dictClusters = {}
  
    _kmeans = None
    
    def __init__(self, dictExpertUsersData):
        print 'instantiated'
        self._dictExpertUsersData = dictExpertUsersData
   
    '''
    Clusters the users based on their locations using the KMeans clustering algorithm
    '''
    def _clusterExperts(self, expertise):
        self._dictClusters.clear()
        usersData = self._dictExpertUsersData[expertise]
        data = empty((len(usersData), 2))
        numClusters = self._dictClusterNum[expertise]#min(4 , len(usersData))
        #print numClusters, ' clusters will be generated'
        self._kmeans = KMeans(n_clusters=numClusters)
        index = 0
        for userData in usersData:
            data[index] = asarray([userData[2], userData[3]], dtype=float)
            index += 1
        
        self._kmeans.fit(data)
        labels = self._kmeans.labels_
        index = 0
        for label in labels:
            clusterName = expertise +' Cluster-' + str(label)
            clusterUserData = usersData[index]
            if clusterName in self._dictClusters:
                self._dictClusters[clusterName].append(clusterUserData)
            else:
                self._dictClusters[clusterName] = [clusterUserData]
            index += 1
        #print 'Done clustering', len(data), ' points'

    '''
    Creates regions corresponding to each expert cluster
    predicted by the clustering algorithm.
    
    '''
    def getExpertRegions(self, expertise):
        #print 'Creating regions for ', expertise
        self._clusterExperts(expertise)
        expertRegions = []
        index = 0
        for clusterName in self._dictClusters:
            expertUsersData = self._dictClusters[clusterName]
            region = self._createExpertRegionWithRandomCenters(expertUsersData, expertise, index)
            #print 'Created ', region.getName(),' with center', region.getCenter()
            expertRegions.append(region)
            index += 1
        #print 'created ', len(expertRegions) , ' for ', expertise
        return expertRegions
              
    '''
    Creates a bounding region for a certain expertise based on the
    location information in user data.
    @param expertUsersData: The expert users' data  for which we want to create a bounding
    region.
    @return: The bounding region corresponding to the expertise.
    '''
    def _createExpertRegionWithRandomCenters(self, expertUsersData, expertise, index):
        #print expertUsersData
        maxLatitude = max(expertUsersData, key=itemgetter(2))[2]
        minLatiude = min(expertUsersData, key=itemgetter(2))[2]
        maxLongitude = max(expertUsersData, key=itemgetter(3))[3]
        minLongitude = min(expertUsersData, key=itemgetter(3))[3]
        leftTop = (maxLatitude, minLongitude)
        rightBottom = (minLatiude, maxLongitude)
        expertRegion = Region(leftTop, rightBottom, expertise + ' Region '+ str(index), isParent=True, expertise = expertise)
        #print 'Coordinates : minlatitude = ', minLatiude, ', maxLatitude = ', maxLatitude
        #print 'minlongitude = ', minLongitude, ', maxlongitude = ', maxLongitude
        return expertRegion
        
def main():
    print 'Main'
    data = DataExtractorFactory.getDataExtractor('expertmodel', 'data/')
    expertsData = data.getAllExpertsData()
    clusterer = UsersClustering(expertsData)
    clusterer.getExpertRegions('tech')
    '''
    clusterer.getExpertRegions('rap')
    clusterer.getExpertRegions('dog')
    clusterer.getExpertRegions('finance')
    '''
    

if __name__ == "__main__":
    main()  
