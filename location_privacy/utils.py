'''
Created on Jan 24, 2014

@author: Himanshu Barthwal
'''
from library.file_io import FileIO
import argparse
import settings
from os.path import join

class Utils:

    @classmethod
    def process_args(cls, args):
        output_directory = ''
        if args[4] == '-output_dir':
            args.pop(0)
            args.pop(3)
            output_directory = args.pop(3)
        else:
            output_directory = settings.stats_data_directory
        job_args = {'output_directory' : output_directory}
        return args, job_args

    @classmethod
    def get_plotclass_key(cls, plotclass):
        return plotclass.__name__.replace('Plot', '')

    @classmethod
    def get_mrjob_class_key(cls, mrJobClass):
        return mrJobClass.__name__.replace('MR', '')

    @classmethod
    def parse_plotter_args(cls):
        parser = argparse.ArgumentParser('The utility generates plots using the data'
                                     ' data generated by the statistics module. The utility requires'
                                     'the path of the data file')

        parser.add_argument('-data_directory',
                            help = 'The path of the data directory',
                            default = settings.stats_data_directory)

        parser.add_argument('-output_directory',
                            help = 'The path of the output directory',
                            default = settings.plots_directory)
        parser.add_argument('-jobargs')
        args = parser.parse_args()
        return args

    @classmethod
    def _write_raw_output(cls, output_filename, key, mr_job, runner):
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            if hasattr(mr_job, 'output_writer'):
                mr_job.output_writer(key, value, output_filename)
            else:
                key = str(key)
                value = str(value)
                FileIO.writeToFile(key + ' ' + value, output_filename)

    @classmethod
    def _write_json_output(cls, output_filename, key, mr_job, runner):
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            if hasattr(mr_job, 'output_writer'):
                mr_job.output_writer(key, value, output_filename)
            else:
                key = str(key)
                value = str(value)
                FileIO.writeToFile(key + ' ' + value, output_filename)

    @classmethod
    def _write_output(cls, output_filename, key, mr_job, runner, output_format):
        if output_format == 'raw':
            cls._write_raw_output(output_filename, key, mr_job, runner)
        elif output_format == 'json':
            cls._write_json_output(output_filename, key, mr_job, runner)

    @classmethod
    def run_mrjob(cls, mr_job_class, runner_args, job_args):
        '''
        Runs the MapReduce job provided as 'mr_job_class'
        with given input files list and the runner arguments
        and writes the output to the provided output file.
        '''
        key = (Utils.get_mrjob_class_key(mr_job_class))
        output_filename = settings.jobsettings[key]['datafile']
        #  The full path of the output file
        output_filename = join(job_args['output_directory'], output_filename)

        #  default output format is raw
        output_format = 'raw'
        if 'output_format' in settings.jobsettings[key]:
            #  If the output format is specified in the settings then use it.
            output_format = settings.jobsettings[key]['output_format']
        mr_job = mr_job_class(args = runner_args)

        with mr_job.make_runner() as runner:
            runner.run()
            print 'Writing data for ', mr_job_class.__name__, ' to ', output_filename
            cls._write_output(output_filename, key, mr_job, runner, output_format)
