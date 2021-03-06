'''
Created on Dec 27, 2013

@author: Himanshu Barthwal
'''
from mrjob.job import MRJob
from cjson import decode
from library.twitter import getDateTimeObjectFromTweetTimestamp
from time import mktime
from operator import itemgetter
from math import ceil
from common_functions import Utils
from settings import jobsettings

class MRExtractTimeSeries(MRJob):
    '''
    Generates a time series of number of daily checkins by the users in the
    data set generated by the TweetsParser.
    '''
    def load_options(self, args):
        super(MRExtractTimeSeries, self).load_options(args)
        key = Utils.get_mrjob_class_key(self.__class__)
        self._start_timestamp = jobsettings[key]['start_timestamp']
        self._end_timestamp = jobsettings[key]['end_timestamp']
        self._bucket_width = jobsettings[key]['bucket_width']

    def __init__(self, *args, **kwargs):
        super(MRExtractTimeSeries, self).__init__(*args, **kwargs)

    def read_checkins(self, _, line):
        if line != '':
            data = decode(line)
            #  If the tweet is geolocated with valid coordinates
            #  then we put it in the checkins bucket for the
            #  corresponding user
            if data['c'] != 'N' and data['c'] != [0.0, 0.0]:
                timestamp = data['t']
                date_time_object = getDateTimeObjectFromTweetTimestamp(timestamp)
                timestamp = mktime(date_time_object.timetuple())
                tweet_id = data['tid']
                checkin = {'tid' :  str(tweet_id) , 't' : timestamp}
                yield data['u'], checkin

    def create_timeseries(self, uid, checkins):
        checkins_list = list(checkins)
        if len(checkins_list) > 15:
            yield uid, checkins_list

    def bucket_time_series(self, uid, time_series):
        sorted_time_series = sorted(time_series, key = itemgetter('t'))
        #  Each bucket is for the count of tweets posted by a user in a day.
        #  The size of each bucket should be specified in seconds
        number_of_buckets = ((self._end_timestamp - self._start_timestamp) / self._bucket_width)
        if number_of_buckets == 0:
            raise Exception("Please check the bucket settings.")
        bucketed_time_series = [0] * number_of_buckets
        for checkin in sorted_time_series:
            time_since_starting_time = checkin['t'] - self._start_timestamp
            bucket_index = int(ceil(time_since_starting_time / self._bucket_width)) - 1
            if bucket_index < number_of_buckets:
                bucketed_time_series[bucket_index] += 1
        yield None, {uid:bucketed_time_series}

    def steps(self):
        return [
                    self.mr(mapper = self.read_checkins,
                                reducer = self.create_timeseries),
                    self.mr(mapper = self.bucket_time_series)
                    ]
def main():
    MRExtractTimeSeries().run()

if __name__ == '__main__':
    main()
