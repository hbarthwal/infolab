'''
Created on Apr 13, 2013

@author: Himanshu Barthwal
'''
from operator import itemgetter
from region import Region
from extractdata import DataExtractor
from sklearn.cluster import KMeans
from numpy import asarray, empty, float


class UsersClustering:
    
    _dictExpertUsersData = {'aggie':[(1445345,.6678, 45,-63)]}
    _dictClusters = {}
    _dictClusterNum = {'coach':9 , 'art':13, 'rap':7, 'player':2, 'vc':6, 'lawyer':8, 'foodie':8, 'nba':7,
                       'economist':4, 'nerd':3, 'hippie':1, 'psychic':7, 'wizard':3, 'actor':7, 'music':10,
                       'farmer':7, 'longhorn':3, 'googler':4, 'economy':4, 'football':5, 'finance':7, 'musician':12,
                       'geek':7, 'aggie':4, 'news':5, 'data':6, 'nfl':6, 'entrepreneur':8, 'consultant':7,
                       'professor':5, 'responder':2, 'dog':7, 'politic':8, 'academia':7, 'tech':8, 'artist':10,
                       'travel':11, 'car dealer':6}

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
            region = self._createExpertRegion(expertUsersData, expertise, index)
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
    def _createExpertRegion(self, expertUsersData, expertise, index):
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
    data = DataExtractor('data/')
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
