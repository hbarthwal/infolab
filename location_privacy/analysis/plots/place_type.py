'''
Created on Jan 25, 2014

@author: Himanshu Barthwal
'''
from matplotlib.pyplot import *
from utils import Utils
from operator import itemgetter
from math import log
import matplotlib as mpl

class PlotPlacesTypeDistribution:

    def __init__(self, datafile):
        self._datafile = datafile

    def plot_data(self, pdf_file, image_filename):
        place_types = []
        reference_counts = []
        for data_row in Utils.get_data_vectors(self._datafile, ' '):
            place_types.append(data_row[0])
            reference_counts.append(int(data_row[1]))
        figure(1, figsize = (6, 6))
        ax = axes([0.1, 0.1, 0.8, 0.8])
        #  The slices will be ordered and plotted counter-clockwise.
        labels = place_types
        total_references = sum(reference_counts)
        #  Eliminate the NA data
        index = place_types.index('NotAvailable')
        place_types.pop(index)
        NA_count = reference_counts.pop(index)
        NA_percentage = 100 * NA_count / float(total_references)
        total_references -= NA_count

        fracs = [count / float(total_references) for count in reference_counts]
        explode = (0, 0, 0, 0, 0)
        mpl.rcParams['font.size'] = 9.0

        pie(fracs, explode = explode, labels = labels, autopct = '%1.1f%%', shadow = False, startangle = 0)
        #  The default startangle is 0, which would start
        #  the Frogs slice on the x-axis.  With startangle=90,
        #  everything is rotated counter-clockwise by 90 degrees,
        #  so the plotting starts on the positive y-axis.

        title('Place Type Distribution: ' + str(NA_percentage) +
              '% tweets dont have a place type, showing the remaining tweets',
              bbox = {'facecolor':'0.8', 'pad':5})
        savefig(pdf_file, format = 'pdf')
        savefig(image_filename)
        clf()


def main():
    plotter = PlotPlacesTypeDistribution('/home/himanshu/data/output/place_type_distribution')
    plotter.plot_data()

if __name__ == '__main__':
    main()
