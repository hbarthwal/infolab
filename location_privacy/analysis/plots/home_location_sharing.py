'''
Created on Jan 25, 2014

@author: Himanshu Barthwal
'''
'''
Created on Jan 25, 2014

@author: Himanshu Barthwal
'''
from matplotlib.pyplot import *
from utils import Utils
import matplotlib as mpl

class PlotUserHomeLocationSharingDistribution:

    def __init__(self, datafile):
        self._datafile = datafile

    def plot_data(self, pdf_file, image_filename):
        categories = []
        tweet_count = []
        for data_row in Utils.get_data_vectors(self._datafile, ' '):
            categories.append(data_row[0])
            tweet_count.append(int(data_row[1]))
        figure(1, figsize = (6, 6))
        ax = axes([0.1, 0.1, 0.8, 0.8])

        #  The slices will be ordered and plotted counter-clockwise.
        labels = categories
        total_references = sum(tweet_count)
        fracs = [count / float(total_references) for count in tweet_count]
        explode = (0, 0)
        mpl.rcParams['font.size'] = 12.0
        pie(fracs, explode = explode, labels = labels, autopct = '%1.1f%%', shadow = False, startangle = 0)
        #  The default startangle is 0, which would start
        #  the Frogs slice on the x-axis.  With startangle=90,
        #  everything is rotated counter-clockwise by 90 degrees,
        #  so the plotting starts on the positive y-axis.

        title('Home Location Sharing ', bbox = {'facecolor':'0.8', 'pad':5})
        savefig(pdf_file, format = 'pdf')
        savefig(image_filename)
        clf()


def main():
    plotter = PlotUserHomeLocationSharingDistribution('/home/himanshu/data/output/user_home_location_sharing')
    plotter.plot_data()

if __name__ == '__main__':
    main()

