'''
Created on Sep 2, 2013

@author: himanshu
'''

from httplib import HTTPSConnection, HTTPS_PORT
from urllib2 import quote
from bs4 import BeautifulSoup
from re import compile

class TwitterResultsFetcher:
    _locations = [('New York', 15),
                   ('San Francisco', 15),
                   ('Chicago', 15),
                   ('Houston', 15)
                 ]
    _topics = [ 'food', 'tech', 'travel', 'entertain']
    
    _twitterURL = 'twitter.com'
    _searchParams = '/search?q=topic%20near%3A"location"%20within%3AXXmi&src=typd&mode=users'
    _resultsDict = {}
    _tagIdRegex = compile('stream-item-user-[\d]+')
    
    
    def __init__(self):
        self._resultsDict = {}

    def _fetchHTML(self, searchURL):
        connection = HTTPSConnection(self._twitterURL, HTTPS_PORT)
        print 'Connection setup done ...'
        connection.request("GET", searchURL)
        print 'Made request..'
        response = connection.getresponse()
        print 'Got response ...Status:', response.status
        html = response.read()
        return html
    
    def _getSearchURL(self, topic, location, radius):
        encodedTopic = quote(topic)
        encodedLocation = quote(location)
        searchURL = self._searchParams.replace('topic', encodedTopic)
        searchURL = searchURL.replace('location',encodedLocation)
        searchURL = searchURL.replace('XX',str(radius))
        print searchURL
        return searchURL
    
    def getTwitterResults(self):
        for location in self._locations:
            for topic in self._topics:
                searchURL = self._getSearchURL(topic, location[0], location[1])
                resultHTML = self._fetchHTML(searchURL)
                print resultHTML
                userIds = self.parseUserIds(resultHTML)
                self._resultsDict[topic + '-' + location[0]] = userIds
        return self._resultsDict
        
        
    def parseUserIds(self, html):
        userIds = []
        parser = BeautifulSoup(html)
        matchingTags = parser.find_all('li')
        for matchingTag in matchingTags:
            print matchingTag.attrs
            if matchingTag.attrs.has_key('data-item-id'):
                userId = matchingTag.attrs['data-item-id']
                if userId != None:
                    userIds.append(userId)
        return userIds
        
        
def main():
    fetcher = TwitterResultsFetcher()
    result = fetcher.getTwitterResults()
    print result, len(result['tech-New York'])

if __name__ == "__main__":
    main()          

    
    


