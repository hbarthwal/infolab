'''
Created on Feb 1, 2014

@author: Himanshu Barthwal
'''
from mrjob.job import MRJob
from cjson import decode
from collections import defaultdict
from settings import jobsettings
from common_functions import Utils

class MRUserGeoTweetCountDistribution(MRJob):
    def configure_options(self):
        super(MRUserGeoTweetCountDistribution, self).configure_options()
        self.add_file_option('--filter_file', help = 'The file containing'
                             ' the uids, to be applied as filter on the data.')
        self.add_passthrough_option('--apply_filter', action = 'store_true',
                                    default = False, dest = 'apply_filter')
        self.add_passthrough_option('--delta',
                                    default = 1, type = 'int', dest = 'delta')

    def load_options(self, args):
        super(MRUserGeoTweetCountDistribution, self).load_options(args)
        filter_filename = self.options.filter_file
        if self.options.apply_filter:
            self._uids = Utils.get_filter_uids(filter_filename)

    def yield_data(self, data):
        if data['c'] != 'N' and data['c'] != [0.0, 0.0]:
            yield data['u'], 1

    def read_data(self, _, line):
        data = decode(line)
        if self.options.apply_filter:
            if data['u'] in self._uids:
                return self.yield_data(data)
        else:
            return self.yield_data(data)

    def aggregate_data(self, uid, tweet_count):
        yield uid, sum(tweet_count)

    def get_bucket_index(self, uid, tweet_count):
        index = tweet_count / float(self.options.delta)
        index = int(round(index)) * self.options.delta
        yield index, 1

    def emit_results(self, index, count):
        yield index , sum(count)

    def steps(self):
        #  Here we use the methods in the base class
        return [self.mr(mapper = self.read_data,
                                combiner = self.aggregate_data,
                                reducer = self.aggregate_data),
                    self.mr(mapper = self.get_bucket_index,
                                reducer = self.emit_results)
                    ]
def main():
    MRUserGeoTweetCountDistribution().run()

if __name__ == '__main__':
    main()

