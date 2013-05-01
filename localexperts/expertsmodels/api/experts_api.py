'''
Created on Mar 30, 2013

@author: Himanshu Barthwal
'''
from io import open
from json import loads
from os.path import join

from expertsmodels.lib.extractdata import DataExtractorFactory
from expertsmodels.lib.expert_impact_model import ExpertImpactAPI

class ExpertsDataAPI:
    
    _expertDataDirectory = '/home/himanshu/workspace/infolab/localexperts/expertsmodels/lib/expertdata/'
    _expertiseDataDirectory = '/home/himanshu/workspace/infolab/localexperts/expertsmodels/lib/expertisedata/'
    
    def __init__(self):
        self._expertiseDataExtractor = DataExtractorFactory.getDataExtractor('expertisemodel', self._expertiseDataDirectory)
        self._expertDataExtractor = DataExtractorFactory.getDataExtractor('expertmodel', self._expertDataDirectory)

    def getExpertiseHeatmapData(self, expertise):
        expertsDataList = self._expertiseDataExtractor.getExpertUsersData(expertise)
        print 'No of entries : ', len(expertsDataList)
        expertsDataListForHeatmap = []
        for expertData in expertsDataList:
            expertDataDict = {'lat': expertData[2],'lng':expertData[3], 'count':expertData[1]}
            expertsDataListForHeatmap.append(expertDataDict)
        return expertsDataListForHeatmap
    
    
    def getExpertHeatmapData(self, expertise, expertId):
        print 'Got request for ', expertId, expertise,'------------------'
        expertsDataList = self._expertDataExtractor.getExpertUsersData(int(expertId), expertise)
        print 'No of entries : ', len(expertsDataList)
        expertsDataListForHeatmap = []
        for expertData in expertsDataList:
            expertDataDict = {'lat': expertData[2],'lng':expertData[3], 'count':expertData[1]}
            expertsDataListForHeatmap.append(expertDataDict)
        return expertsDataListForHeatmap
    
    
        
class ExpertsSearchAPI:
    _dataDirectory = '/home/himanshu/workspace/infolab/localexperts/expertsmodels/lib/expertdata/'
    _cacheFile = 'models.json'
    _expertImpactAPI = ExpertImpactAPI(_dataDirectory, _cacheFile)
    _profileInfoDict = {}
    _profileDataFileName = 'user_profiles.json'
    
    def __init__(self):
        self._populateProfileData()
    
    def _populateProfileData(self):
        filename = join(self._dataDirectory,self._profileDataFileName)
        with open(filename, 'r+') as profilesData:
            for profileData in profilesData:
                profileData = loads(profileData)
                description = profileData['description']
                username = profileData['screen_name']
                userLocation = profileData['location']
                imageUrl = 'http://icons.iconarchive.com/icons/deleket/scrap/256/User-icon.png'
                userId = profileData['_id']
                userInfoDict = {'user_name': username,
                                'user_description': description,
                                'profile_image_url':imageUrl,
                                'user_location':userLocation}
                
                self._profileInfoDict[userId] = userInfoDict
    
    
    def getExperts(self, query, queryLocation):
        print 'Getting experts for ', query
        rankedExpertsList = self._expertImpactAPI.getRankedExperts(query ,queryLocation)
        rankedUsersDetails = []
        for userId in rankedExpertsList:
            userProfileDict = self._profileInfoDict[userId]
            rankedUsersDetails.append(userProfileDict)
        return rankedUsersDetails
        
def main():
    searchAPI = ExpertsSearchAPI()
    
    
if __name__ == "__main__":
    main()    
    
    
    
    
    
    
    
    
