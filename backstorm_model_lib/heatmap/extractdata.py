'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
from os import listdir
from os.path import isfile, join

class DataExtractor:
#                 { expertise :[( userId,   ??,  latitude, longitude),(..)..]}
    expertUsersData = {'tech' : [(23423523, .98763, -98.466 , 97.577)]}
    
    def __init__(self, dataDirectory):
        self.expertUsersData.clear()
        self._populateData(dataDirectory)
    
    
    def _populateData(self, dataDirectory):
        filenames = []
        # getting the filenames of all the files with the user expertise geographical data
        for f in listdir(dataDirectory):
                if isfile(join(dataDirectory, f)) and '.txt' in join(dataDirectory, f):
                    filenames.append(join(dataDirectory, f))
        # extracting the data from each file corresponding to an expertise         
        for filename in filenames:            
            self._populateDataForExpertise(filename)
                      
    def _extractExpertise(self, filename):
        return filename.split('_')[-1:][0].split('.')[0]
        
    
    def _populateDataForExpertise(self, filename):   
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
                expertsDataList.append((userId, expertRank, latitude, longitude))
        self.expertUsersData[expertise] = expertsDataList
        
    def displayData(self, expertise):
        print '------------------'
        print self.expertUsersData
        

def main():
    print 'Main'
    dataDirectory = '/home/himanshu/workspace/backstorm_model_lib/heatmap/data/expert_locations'
    data = DataExtractor(dataDirectory)
    data.displayData('academia')
        
    
    
if __name__ == "__main__":
    main()    
        