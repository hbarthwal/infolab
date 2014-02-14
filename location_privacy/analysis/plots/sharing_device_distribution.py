'''
Created on Jan 25, 2014

@author: Himanshu Barthwal
'''
from matplotlib.pyplot import *
from utils import Utils
import random
from operator import itemgetter
import matplotlib as mpl

class PlotSharingDeviceDistribution:

    def __init__(self, datafile):
        self._datafile = datafile

    def plot_data(self, pdf_file, image_filename):
        data_dict = {}
        for data_row in Utils.get_data_vectors(self._datafile, '|'):
            data_dict[data_row[0]] = int(data_row[1])
        fig = figure(1, figsize = (6, 6))
        ax = axes([0.2, 0.2, 0.6, 0.6])

        #  The slices will be ordered and plotted counter-clockwise.
        data_dict = sorted(data_dict.iteritems(), key = itemgetter(1), reverse = True)
        total_tweet_count_original = sum(float(data[1]) for data in data_dict)
        data_dict = data_dict[0:5] + data_dict[10:12] + data_dict[6:9] + data_dict[13:15]

        total_tweet_count = sum(float(data[1]) for data in data_dict)
        application_names = list(data[0] for data in data_dict)
        tweet_percentage = 100 * (total_tweet_count / float(total_tweet_count_original))
        fracs = [float(data[1]) / total_tweet_count for data in data_dict]
        mpl.rcParams['font.size'] = 6.0
        pie(fracs, labels = application_names, autopct = '%1.1f%%', shadow = False, startangle = 0)
        title('Tweet sources Distribution: Showing top 15 tweet sources which generate ' +
              str(tweet_percentage) +
               '% of the total tweets', bbox = {'facecolor':'0.8', 'pad':5})
        savefig(pdf_file, format = 'pdf')
        savefig(image_filename)
        clf()


def main():
    plotter = PlotSharingDeviceDistribution('/home/himanshu/data/output/sharing_device_distribution')
    plotter.plot_data('sample')

if __name__ == '__main__':
    main()
