'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
from os import listdir
from os.path import isfile, join, dirname

class DataExtractor:
#                 { expertise :[( userId,   confidence,  latitude, longitude),(..)..]}
    _expertUsersData = {'tech' : [[23423523, .98763, -98.466 , 97.577]]}
    _dataDirectory = ''
    _dataFileNamePartOne = 'expert_locations_for_'
    _dataFileNamePartTwo = '_full_data.txt'
    _dictRegionUserDistribution = {}
    _filterList = [
                      { 
                       'leftTopCoordinates' : (50, -125),
                       'rightBottomCoordinates' : (49.255, -122),
                       'region' : 'USA'
                      }
                   ]
    '''
                      ,
                      { 
                       'leftTopCoordinates' : (39.92, -124.96),
                       'rightBottomCoordinates' : (34.13, -117.73),
                       'region' : 'Bay Area'
                      },
                      { 
                       'leftTopCoordinates' : (37.3, -106.7),
                       'rightBottomCoordinates' : (25.8, -89.0),
                       'region':'Texas'
                      }
    '''
                    
    
    '''
    Instantiates the object for DataExtractor
    @param dataDirectory: The directory in which the data files are residing
    '''
    def __init__(self, dataDirectory):
        self._expertUsersData.clear()
        self._dataDirectory = dataDirectory
        
      
    #filters the user data for United States only
    
    '''
    Checks if a location belongs to the US region.
    @param userData: The user data for which we want to test whether it lies in US
    @return: True if the user lies in the US, False otherwise.
    '''

    def _initializeRegionDistributionDict(self, expertise):
        dictRegionUserDistribution = {}
        for filterCoordinates in self._filterList:
            region = filterCoordinates['region']
            dictRegionUserDistribution[region] = 0
        self._dictRegionUserDistribution[expertise] = dictRegionUserDistribution
        return filterCoordinates, region

    def _isFilterable(self, userData):
        for filterCoordinates in self._filterList:        
            rightBottomCoordinates = filterCoordinates['rightBottomCoordinates']
            leftTopCoordinates = filterCoordinates['leftTopCoordinates']
            region = filterCoordinates['region']
            if userData[2] >= rightBottomCoordinates[0] and userData[2] <= leftTopCoordinates[0]:
                if userData[3] <= rightBottomCoordinates[1] and userData[3] >= leftTopCoordinates[1]:
                    self._dictRegionUserDistribution[userData[4]][region] += 1
                    return True
        return False
   
    '''
    Populates data for a given expertise from the data files.
    @param dataDirectory: the directory in which the data files reside
    @param expertise: the expertise for which we want to populate the data if expertise = "all"
    then the data will be populated for all the possible expertise values
    '''
    def populateData(self, dataDirectory, expertise = 'all'):
        if expertise == 'all':
            filenames = []
            # getting the filenames of all the files with the user expertise geographical data
            for f in listdir(dataDirectory):
                    if isfile(join(dataDirectory, f)) and '.txt' in join(dataDirectory, f):
                        filenames.append(join(dataDirectory, f))
            # extracting the data from each file corresponding to an expertise         
            for filename in filenames:            
                self._populateDataFromFile(filename)
        
        else :
            self._populateDataForExpertise(expertise)
    '''
    Generates the file name from the expertise
    It assumes a pattern in the filenames 
    @param expertise: The expertise for which we want to generate the filename
    @return: The filename corresponding to the expertise 
    '''        
    def _getFileNameFromExpertise(self, expertise):
        filename = self._dataFileNamePartOne + expertise + self._dataFileNamePartTwo
        return join(self._dataDirectory, filename)
    
    '''
    Extracts the expertise from a given filename
    @return:  The expertise corresponding to the filename
    '''          
    def _extractExpertise(self, filename):
        filename = filename.replace(dirname(filename) + '/','')
        filename = filename.replace(self._dataFileNamePartOne,'')
        expertise = filename.replace(self._dataFileNamePartTwo, '')
        return expertise
        
    '''
    Populates the data for a given expertise
    @param expertise: the expertise for which we want to populate the data if expertise = "all"
    then the data will be populated for all the possible expertise values
    '''
    def _populateDataForExpertise(self, expertise):
        filename = self._getFileNameFromExpertise(expertise)
        self._populateDataFromFile(filename)
    
    '''
    Populates the data from file 
    @param filename: The filename from which the data is to be extracted
    '''
    def _populateDataFromFile(self, filename):   
        # extracting the expertise from filename
        expertise = self._extractExpertise(filename)
        self._initializeRegionDistributionDict(expertise)
        expertsDataList = []
        count = 0
        with open(filename) as expertsData:
            for expertData in expertsData:
                rawData = expertData.split('\t')
                userId = rawData[0].strip()
                expertRank = rawData[1].strip()
                latitude = rawData[2].strip()
                longitude = rawData[3].strip()
                userData = [int(userId), float(expertRank), float(latitude), float(longitude), expertise]
                # We restrict our study to United States only
                if self._isFilterable(userData):
                    expertsDataList.append(userData)
                else:
                    count += 1
        #print expertise, ': Got ', len(expertsDataList), ' users out of ', count, ' filtered !!'
        if len(expertsDataList) > 0:
            self._expertUsersData[expertise] = expertsDataList
        
        if expertise == 'tech':
            print 'The region distribution of the points for ', expertise ,' is :', self._dictRegionUserDistribution[expertise]
    
    '''
    Displays the extracted data
    '''
    def displayData(self, expertise):
        print '------------------'
        print self._expertUsersData[expertise]
    
    '''
    Gets the expertusers data 
    @param expertise: The expertise for which the usersdata is to be returned
    @return: userdata corresponding to the given expertise
    '''
    def getExpertUsersData(self, expertise):
        if expertise not in self._expertUsersData:
            self.populateData(self._dataDirectory, expertise)
            return self._expertUsersData[expertise]
        return self._expertUsersData[expertise]
    
    '''
    Gets all the expertusers data 
    @return: The dictionary containing usersdata for all the expertise
    '''
    def getAllExpertsData(self):
        if len(self._expertUsersData) == 0:
            self.populateData(self._dataDirectory, expertise='all')
        return self._expertUsersData

def main():
    print 'Main'
    dataDirectory =  'data/'
    data = DataExtractor(dataDirectory)
    data.getExpertUsersData('tech')
        
    
if __name__ == "__main__":
    main()    
        