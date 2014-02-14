'''
Created on Dec 20, 2013
@author: Himanshu Barthwal
'''
import os, gzip, cjson
import argparse
from library.twitter import TweetFiles, getStringRepresentationForTweetTimestamp, \
    getDateTimeObjectFromTweetTimestamp
from library.file_io import FileIO
from library.geo import isWithinBoundingBox, getCenterOfMass, \
    getHaversineDistance
from settings import us_boundary
from bs4 import BeautifulSoup
from os.path import exists
from os import walk
import sys


class TweetParser:
    '''
    Provides the functionality of parsing the files  in the hierarchy 
    of the twitter data at Infolab, extracting the checkin data
    and populating it into files such that each file represents monthly data.
    '''
    @classmethod
    def tweetFilesIterator(cls, year, months, input_dir, output_dir):
        checkinsFile = output_dir + '%s' % year + '_%s'
        bdeDataFolder = input_dir + '%s' % year + '/%s/%s/'
        for month in months:
            outputFile = checkinsFile % month
            for day in range(1, 32):
                tweetsDayFolder = bdeDataFolder % (month, day)
                if exists(tweetsDayFolder):
                    for _, _, files in walk(tweetsDayFolder):
                        for file in files:
                            yield outputFile, tweetsDayFolder + file

    @classmethod
    def _get_social_status(cls, data):
        social_status = 'N'
        #  Calculate social status
        followers = data['user']['followers_count']
        freinds = data['user']['friends_count']
        if freinds != 0:
            social_status = followers / float(freinds)
        return str(social_status)

    @classmethod
    def _get_coordinates(cls, data):
        place_type = 'N'
        coordinates = 'N'
        try:
            #  Extract the coordinates of the checkin
            if 'geo' in data and data['geo'] != None:
                coordinates = data['geo']['coordinates']
            elif 'coordinates'in data and data['coordinates'] != None:
                coordinates = data['coordinates']
            if 'place' in data and data['place'] != None and \
               'place_type' in data['place'] and data['place']['place_type'] != None:
            #  Extract the place_type
                place_type = data['place']['place_type']
        except:
            print 'Error while extracting coordinates'
            print 'Data:', data
            print sys.exc_info()
        return coordinates, place_type

    @classmethod
    def _get_tweet_source(cls, data):
        #  Extract the tweet source
        soup = BeautifulSoup(data['source'])
        source = soup.get_text(',', strip = True)
        return  source

    @classmethod
    def getTweetObject(cls, data):
        tweet_data = {}
        if 'user' not in data:
            return 0
        social_status = cls._get_social_status(data)
        coordinates, place_type = cls._get_coordinates(data)
        source = cls._get_tweet_source(data)
        timestamp = data['created_at']
        #  Populate the data into a dictionary
        tweet_data['u'] = data['user']['id']
        tweet_data['tid'] = data['id']
        tweet_data['ss'] = social_status
        tweet_data['sc'] = data['user']['statuses_count']
        tweet_data['l'] = data['user']['location']
        tweet_data['src'] = source
        tweet_data['c'] = coordinates
        tweet_data['p'] = place_type
        tweet_data['t'] = timestamp
        tweet_data['ge'] = data['user']['geo_enabled']
        tweet_data['uc'] = data['user']['created_at']
        #  converting to tab separated format
        return tweet_data

    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser('The utility parses the tweet data in the'
                                     ' infolab servers, for a given range of months of an year'
                                     ' and writes them into a file in the given output directory.')
        parser.add_argument('-input_directory',
                            help = 'The input directory where the twitter data is residing.',
                            default = '/mnt/chevron/bde/Data/TweetData/GeoTweets/')
        parser.add_argument('-output_directory',
                            help = 'The output directory where the parsed twitter data is to be written.',
                            default = './')
        parser.add_argument('-year',
                            help = 'The year for which the data is to be parsed..',
                            default = '2013')
        parser.add_argument('-months',
                            help = 'Comma separated months for which the data is to be parsed.',
                            default = '1,3')
        args = parser.parse_args()
        return args

def main():
    args = TweetParser.parse_args()
    months = args.months.split(',')
    print 'Starting to parse tweet files...'
    for outputFile, file in TweetParser.tweetFilesIterator(args.year, months, args.input_directory, args.output_directory):
        print 'Parsing: %s' % file
        with gzip.open(file, 'rb') as data_file:
            print 'Opened file..'
            for line in data_file:
                try:
                    data = cjson.decode(line)
                    tweet = TweetParser.getTweetObject(data)
                    if tweet != 0:
                        FileIO.writeToFileAsJson(tweet, outputFile)
                except:
                    print 'Exception'
                    print sys.exc_info()
    print 'Data extracted ! !'

if __name__ == '__main__':
    main()

