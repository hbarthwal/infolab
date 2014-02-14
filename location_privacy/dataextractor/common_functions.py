'''
Created on Feb 9, 2014

@author: Himanshu Barthwal
'''
from math import ceil

class Utils:
    @classmethod
    def get_mrjob_class_key(cls, mrJobClass):
        return mrJobClass.__name__.replace('MR', '')

class CoordinatesSharing:
    @classmethod
    def read_data(cls, data):
        if data['c'] != 'N' and data['c'] != [0.0, 0.0]:
            yield str(data['u']) , '1-y'
        elif data['ge']:
            yield str(data['u']) , '1-g'
        else:
            yield str(data['u']) , '1-n'
    @classmethod
    def get_index(cls, checkins):
            total_tweets = checkins['y'] + checkins['n'] + checkins['g']
            selectively_non_geo_tweet_percentage = 100 * (checkins['g'] / float(total_tweets))
            index = int(ceil(selectively_non_geo_tweet_percentage))
            if index > 100:
                index = 100
            return index

    @classmethod
    def aggregate_data(cls, uid, data):
            yes_count = 0
            no_count = 0
            ge_count = 0
            for line in data:
                line = line.split('-')
                count = int(line[0])
                has_coordinates = line[1]
                if has_coordinates == 'n':
                    no_count += count
                elif has_coordinates == 'y':
                    yes_count += count
                elif has_coordinates == 'g':
                    ge_count += count
            yield uid, {'y':yes_count, 'n': no_count, 'g':ge_count}

