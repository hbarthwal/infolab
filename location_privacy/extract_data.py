'''
Created on Feb 9, 2014

@author: Himanshu Barthwal
'''
from utils import Utils
import settings
import sys

class DataExtractor:
    @classmethod
    def extract_data(cls, args):
        data_extractors = settings.data_extractors
        runner_args, job_args = Utils.process_args(args)
        for data_extractor in data_extractors:
            Utils.run_mrjob(data_extractor, runner_args, job_args)

def main():
    args = sys.argv
    DataExtractor.extract_data(args)

if __name__ == '__main__':
    main()
