'''
Created on Jan 25, 2014

@author: Himanshu Barthwal
'''
import matplotlib.pyplot as P
from utils import Utils
from operator import itemgetter
from math import log

class PlotUserGeoTweetCountDistribution:

    def __init__(self, datafile):
        self._datafile = datafile

    def plot_data(self, pdf_file, image_filename):
        data_points = []
        total_user_count = 0
        total_tweet_count = 0
        for data_row in Utils.get_data_vectors(self._datafile, ' '):
            num_tweets = int(data_row[0])
            user_count = int(data_row[1])
            total_user_count += user_count
            total_tweet_count += num_tweets
            data_points.append((num_tweets, user_count))
        bins = []
        user_count = []
        for data_point in sorted(data_points, key = itemgetter(0)):
            bins.append(log(data_point[0]))    #  / float(total_tweet_count))
            user_count.append(log(data_point[1]))    #  / float(total_user_count))
        _, axes = P.subplots()
        axes.plot(user_count, bins, 'ro')
        axes.set_ylabel('log(GeoTweet Count)')
        axes.set_xlabel('log(User Count)')
        P.savefig(pdf_file, format = 'pdf')
        P.savefig(image_filename)
        P.clf()

def main():
    plotter = PlotUserGeoTweetCountDistribution('/home/himanshu/data/output/user_geotweets_count')
    plotter.plot_data()

if __name__ == '__main__':
    main()

