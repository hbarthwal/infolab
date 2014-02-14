'''
Created on Jan 24, 2014

@author: Himanshu Barthwal
'''
from os.path import join
from utils import Utils
from matplotlib.backends.backend_pdf import PdfPages
import settings

class PlotsGenerator:
    @classmethod
    def generate_plots(cls, data_directory, output_directory):
        plotters = settings.plotters
        output_pdf_file = join(output_directory, settings.plot_pdf_file)
        pp = None
        try:
            pp = PdfPages(output_pdf_file)
            for plotclass in plotters:
                    key = Utils.get_plotclass_key(plotclass)
                    data_file_name = settings.jobsettings[key]['datafile']
                    image_file = join(output_directory, settings.jobsettings[key]['plot_image_file'])
                    data_file_name = join(data_directory, data_file_name)
                    plotter = plotclass(data_file_name)
                    plotter.plot_data(pp, image_file)
        finally:
            pp.close()

def main():
    args = Utils.parse_plotter_args()
    PlotsGenerator.generate_plots(args.data_directory, args.output_directory)

if __name__ == '__main__':
    main()
