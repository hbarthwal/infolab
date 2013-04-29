'''
Created on Mar 24, 2013

@author: Himanshu Barthwal
'''
from os import listdir
from os.path import isfile, join, dirname, exists
from settings import Settings
from json import loads
from pickle import load, dump
from pprint import pprint
from stemming import porter2


'''
Factory for data extractors.
'''
class DataExtractorFactory(object):
    @staticmethod
    def getDataExtractor(extractorType, dataDirectory):
             
        ##############################################################################################
        
        class CommonUtils:
            '''
            Generates the file name from the expertise
            It assumes a pattern in the filenames 
            @param expertise: The expertise for which we want to generate the filename
            @return: The filename corresponding to the expertise 
            '''  
            @staticmethod      
            def getFileNameFromExpertise(dataDirectory, expertise):
                filename = Settings.dataFileNamePartOne + expertise + Settings.dataFileNamePartTwo
                return join(dataDirectory, filename)
            
            '''
            Extracts the expertise from a given filename
            @return:  The expertise corresponding to the filename
            '''         
            @staticmethod 
            def extractExpertise(filename):
                filename = filename.replace(dirname(filename) + '/', '')
                filename = filename.replace(Settings.dataFileNamePartOne, '')
                expertise = filename.replace(Settings.dataFileNamePartTwo, '')
                return expertise
        
                 
            '''
            Checks if a location belongs to the US region.
            @param userData: The user data for which we want to test whether it lies in US
            @return: True if the user lies in the US, False otherwise.
            '''
            @staticmethod
            def isFilterable(userData):
                for filterCoordinates in Settings.filterList:        
                    rightBottomCoordinates = filterCoordinates['rightBottomCoordinates']
                    leftTopCoordinates = filterCoordinates['leftTopCoordinates']
                    if userData[2] >= rightBottomCoordinates[0] and userData[2] <= leftTopCoordinates[0]:
                        if userData[3] <= rightBottomCoordinates[1] and userData[3] >= leftTopCoordinates[1]:
                            return True
                return False
        
        '''
        Data extractor for generating models for different expertise topics.
        '''
        class ExpertiseModelDataExtractor:
        #                      { expertise :[( userId,   confidence,  latitude, longitude),(..)..]}
            _expertUsersData = {'tech' : [[23423523, .98763, -98.466 , 97.577]]}
            _dataDirectory = ''
            _dictRegionUserDistribution = {}

            '''
            Instantiates the object for DataExtractor
            @param dataDirectory: The directory in which the data files are residing
            '''
            def __init__(self, dataDirectory):
                self._expertUsersData.clear()
                self._dataDirectory = dataDirectory
                
              
            # filters the user data for United States only
            
            '''
            Initializes the dictRegionUserDistribution dictionary mainly used for 
            debugging purposes.
            '''
                
            def _initializeRegionDistributionDict(self, expertise):
                dictRegionUserDistribution = {}
                for filterCoordinates in Settings.filterList:
                    region = filterCoordinates['region']
                    dictRegionUserDistribution[region] = 0
                self._dictRegionUserDistribution[expertise] = dictRegionUserDistribution
            
            '''
            Checks if a location belongs to the US region.
            @param userData: The user data for which we want to test whether it lies in US
            @return: True if the user lies in the US, False otherwise.
            '''
            def _isFilterable(self, userData):
                for filterCoordinates in Settings.filterList:        
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
            def populateData(self, dataDirectory, expertise='all'):
                
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
            Populates the data for a given expertise
            @param expertise: the expertise for which we want to populate the data if expertise = "all"
            then the data will be populated for all the possible expertise values
            '''
            def _populateDataForExpertise(self, expertise):
                filename = CommonUtils.getFileNameFromExpertise(self._dataDirectory, expertise)
                self._populateDataFromFile(filename)
            
            '''
            Populates the data from file 
            @param filename: The filename from which the data is to be extracted
            '''
            def _populateDataFromFile(self, filename):   
                # extracting the expertise from filename
                expertise = CommonUtils.extractExpertise(filename)
                self._initializeRegionDistributionDict(expertise)
                expertsDataList = []
                count = 0
                with open(filename) as expertsData:
                    for expertData in expertsData:
                        if count == Settings.maxExperts:
                            break
                        rawData = expertData.split('\t')
                        userId = rawData[0].strip()
                        expertRank = rawData[1].strip()
                        latitude = rawData[2].strip()
                        longitude = rawData[3].strip()
                        userData = [int(userId), float(expertRank), float(latitude), float(longitude), expertise]
                        # We restrict our study to United States only
                        if self._isFilterable(userData):
                            expertsDataList.append(userData)
                            count += 1
                            
                if len(expertsDataList) > 0:
                    self._expertUsersData[expertise] = expertsDataList
                
                #print 'The region distribution of the points for ', expertise , ' is :', self._dictRegionUserDistribution[expertise]
            
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

        
        ##############################################################################################
        
        '''
        Data extractor for generating models for individual experts.
        Most of the functionality is just a wrapper over the ExpertiseModelDataExtractor.
        '''
        class ExpertModelDataExtractor:
            _dataDirectory = ''
            _dictRegionUserDistribution = {}
            _userExpertiseDict = {}
            _dictionaryDumpFileName = 'userDataDict'
            _currentExpertise = ''
            
            '''
            Instantiates the object for DataExtractor
            @param dataDirectory: The directory in which the data files are residing
            '''
            def __init__(self, dataDirectory):
                self._dataDirectory = dataDirectory
            
            def getExpertIdsList(self, expertise):
                return self._userExpertiseDict[expertise].keys()
           
            def getExpertiseList(self):
                return self._userExpertiseDict.keys()
           
            def setCurrentExpertise(self, expertise):
                self._currentExpertise = expertise 
           
            def _pruneData(self):
                for expertise in self.getExpertiseList():
                    for expertUserId in self.getExpertIdsList(expertise):
                        if len(self._userExpertiseDict[expertise][expertUserId]) <= 20:
                            self._userExpertiseDict[expertise].pop(expertUserId) 
            '''
            Populates the data for a given expertise
            @param expertise: the expertise for which we want to populate the data if expertise = "all"
            then the data will be populated for all the possible expertise values
            '''
            def _populateExpertUserIdsForExpertise(self, expertise):
                filename = CommonUtils.getFileNameFromExpertise(self._dataDirectory ,expertise)
                self._populateExpertUserIdsFromFile(filename)
            
            '''
            Populates the expert users ids from file 
            @param filename: The filename from which the data is to be extracted
            '''
            def _populateExpertUserIdsFromFile(self, filename):   
                # extracting the expertise from filename
                expertise = CommonUtils.extractExpertise(filename)
                expertsDataDict = {}
                count = 0
                with open(filename) as expertsData:
                    for expertUserId in expertsData:
                        if count == 20:
                            break
                        expertsDataDict[int(expertUserId.strip())] = []
                        count += 1
                            
                if len(expertsDataDict) > 0:
                    self._userExpertiseDict[expertise] = expertsDataDict
                
                #print 'The expert users for ', expertise , ' are :'
                #print expertsDataDict.keys()
           
           
            '''
            Populates data for a given expertise from the data files.
            @param dataDirectory: the directory in which the data files reside
            @param expertise: the expertise for which we want to populate the data if expertise = "all"
            then the data will be populated for all the possible expertise values
            '''
            def _populateExpertUserIds(self, dataDirectory, expertise='all'):
                if expertise == 'all':
                    filenames = []
                    # getting the filenames of all the files with the user expertise geographical data
                    for f in listdir(dataDirectory):
                            if isfile(join(dataDirectory, f)) and '.txt' in join(dataDirectory, f):
                                filenames.append(join(dataDirectory, f))
                    # extracting the data from each file corresponding to an expertise         
                    for filename in filenames:            
                        self._populateExpertUserIdsFromFile(filename)
                
                else :
                    self._populateExpertUserIdsForExpertise(expertise)
           
            '''
            Populates data for a given expertise from the data files.
            @param dataDirectory: the directory in which the data files reside
            @param expertise: the expertise for which we want to populate the data if expertise = "all"
            then the data will be populated for all the possible expertise values
            '''
            def populateData(self, dataDirectory, expertise):
                dumpFile = join(dataDirectory, self._dictionaryDumpFileName)
                if exists(dumpFile):
                    self._userExpertiseDict = load(open(dumpFile,'rb'))
                    return
                
                self._populateExpertUserIds(dataDirectory, expertise)
                self._populateUserDataFromFile()
                self._pruneData()
                dump(self._userExpertiseDict, open(dumpFile, 'wb'))
            
            '''
            Populates the data from file 
            @param filename: The filename from which the data is to be extracted
            '''
            def _populateUserDataFromFile(self):   
                count = 0
                filename = join(self._dataDirectory, Settings.userDataFileName)
                with open(filename) as expertsData:
                    for expertData in expertsData:
                        if count == Settings.maxExperts:
                            break
                        jsonData = loads(expertData)
                        userId = jsonData['list_creator_id']
                        expertRank = 1
                        latitude = jsonData['list_creator_lat']
                        longitude = jsonData['list_creator_lng']
                        expertUserId = jsonData['user_id']
                        listName = jsonData['list_name'].strip()
                        
                        expertise = porter2.stem(listName)
                        #print expertise , ' is the expertise'
                        userData = [int(userId), float(expertRank), float(latitude), float(longitude), expertUserId]
                        
                        if expertise in self._userExpertiseDict: 
                            if expertUserId in self._userExpertiseDict[expertise]:
                                # We restrict our study to restricted regions defined by filters in Settings.py
                                if CommonUtils.isFilterable(userData):
                                    self._userExpertiseDict[expertise][expertUserId].append(userData)
                                    count += 1
                                
                            
            
            '''
            Gets the expertusers data 
            @param expertise: The expertise for which the usersdata is to be returned
            @return: userdata corresponding to the given expertise
            '''
            def getExpertUsersData(self, expertUserId, expertise = ''):
                if expertise == '':
                    expertise = self._currentExpertise
                if expertise not in self._userExpertiseDict:
                    self.populateData(self._dataDirectory, expertise)
                    return self._userExpertiseDict[expertise][expertUserId]
                return self._userExpertiseDict[expertise][expertUserId]
            
            
            '''
            Gets the expertusers data 
            @param expertise: The expertise for which the usersdata is to be returned
            @return: userdata corresponding to the given expertise
            '''
            def getAllExpertsData(self, expertise = ''):
                if expertise == '':
                    expertise = self._currentExpertise 
                if expertise in self._userExpertiseDict:
                    dictUserData = {}
                    for expertUserId in self._userExpertiseDict[expertise]:
                        usersData = self._userExpertiseDict[expertise][expertUserId]
                        dictUserData[expertUserId] = [userData for userData in usersData]
                    return dictUserData
            
            
            '''
            Displays the extracted data
            '''
            def displayData(self):
                print '------------------'
                for expertise in self._userExpertiseDict:
                    print '-----', expertise, '------'
                    for expertUserId in self._userExpertiseDict[expertise]:
                        numberOfUsers = len(self._userExpertiseDict[expertise][expertUserId])
                        if numberOfUsers > 0:
                            print '        ', expertUserId, ' has ', numberOfUsers,' users'            
            
        #################################################################################################################
        
        if extractorType == 'expertisemodel':
            return ExpertiseModelDataExtractor(dataDirectory)
        elif extractorType == 'expertmodel':
            return ExpertModelDataExtractor(dataDirectory)
        else:
            raise RuntimeError("No suitable extractor found for " + type + ' type')
        
        
        
def main():
    print 'Main'
    dataDirectory = 'expertdata/'
    dataExtractor = DataExtractorFactory.getDataExtractor('expertmodel', dataDirectory)
    dataExtractor.populateData(dataDirectory, 'all')
    print dataExtractor.displayData()
    
if __name__ == "__main__":
    main()    
        
