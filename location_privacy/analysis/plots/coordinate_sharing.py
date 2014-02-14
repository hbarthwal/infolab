'''
Created on Jan 24, 2014

@author: Himanshu Barthwal
'''
import matplotlib.pyplot as P
import matplotlib as mpl
from utils import Utils
from operator import itemgetter

class PlotUserCoordinatesSharingDistribution:
    def __init__(self, datafile):
        self._datafile = datafile

    def plot_data(self, pdf_file, image_filename):
        data_points = []
        total = 0
        for data_row in Utils.get_data_vectors(self._datafile, ' '):
            bin = int(float(data_row[0]))
            data = int(float(data_row[1]))
            total += data
            data_points.append((bin, data))
        bins = []
        data = []
        for data_point in sorted(data_points, key = itemgetter(0)):
            bins.append(data_point[0])
            percentage = 100 * data_point[1] / float(total)
            data.append(percentage)
        P.bar(bins, data, width = 1, color = 'r')
        mpl.rcParams['font.size'] = 10.0
        P.xlabel('Geotagged tweet percentage')
        P.ylabel('Users percentage')
        P.savefig(pdf_file, format = 'pdf')
        P.savefig(image_filename)
        P.clf()


def main():
    plotter = PlotUserCoordinatesSharingDistribution('/home/himanshu/data/stats/user_coordinates_sharing')
    plotter.plot_data('coordinate_sharing', 'coordinate_sharing.png')

if __name__ == '__main__':
    main()




