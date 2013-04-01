'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
from os import listdir
from os.path import isfile, join

class DataExtractor:
#                 { expertise :[( userId,   ??,  latitude, longitude),(..)..]}
    _expertUsersData = {'tech' : [(23423523, .98763, -98.466 , 97.577)]}
    _dataDirectory = ''
    
    def __init__(self, dataDirectory):
        self._expertUsersData.clear()
        self._dataDirectory = dataDirectory
      
    #filters the user data for United States only
    def _isPointInUS(self, userData):
        rightBottomCoordinates = (25, -68)
        leftTopCoordinates = (47, -122)
        if userData[2] >= rightBottomCoordinates[0] and userData[2] <= leftTopCoordinates[0]:
            if userData[3] <= rightBottomCoordinates[1] and userData[3] >= leftTopCoordinates[1]:
                return True
        return False
                
    
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
            
    def _getFileNameFromExpertise(self, expertise):
        return join(self._dataDirectory,'expert_locations_for_' + expertise +'.txt')
              
    def _extractExpertise(self, filename):
        return filename.split('_')[-1:][0].split('.')[0]
        
    def _populateDataForExpertise(self, expertise):
        filename = self._getFileNameFromExpertise(expertise)
        self._populateDataFromFile(filename)
    
    def _populateDataFromFile(self, filename):   
        # extracting the expertise from filename
        expertise = self._extractExpertise(filename)
        expertsDataList = []
        with open(filename) as expertsData:
            for expertData in expertsData:
                rawData = expertData.split('\t')
                userId = rawData[0].strip()
                expertRank = rawData[1].strip()
                latitude = rawData[2].strip()
                longitude = rawData[3].strip()
                userData = (int(userId), float(expertRank), float(latitude), float(longitude))
                # We restrict our study to United States only
                if self._isPointInUS(userData):
                    expertsDataList.append(userData)
        self._expertUsersData[expertise] = expertsDataList
        
    def displayData(self, expertise):
        print '------------------'
        print self._expertUsersData[expertise]
    
    def getExpertUsersData(self, expertise):
        if expertise not in self._expertUsersData:
            self.populateData(self._dataDirectory, expertise)
            return self._expertUsersData[expertise]
        return self._expertUsersData[expertise]
    
    def getAllExpertsData(self):
        if len(self._expertUsersData) > 0:
            return self._expertUsersData

def main():
    print 'Main'
    dataDirectory =  '/home/himanshu/workspace/infolab/localexperts/expertsmodels/lib/data/expert_locations'
    data = DataExtractor(dataDirectory)
    data.getExpertUsersData('dog')
    data.displayData('dog')
        
    
    
if __name__ == "__main__":
    main()    
        