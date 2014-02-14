'''
Created on Jan 14, 2014

@author: Himanshu Barthwal
'''
from utils import Utils
import settings
import sys


class StatisticsGenerator:
    @classmethod
    def generate_stats(cls, args):
        runner_args, job_args = Utils.process_args(args)
        stats_generators = settings.stats_generators
        for stat_generator in stats_generators:
            Utils.run_mrjob(stat_generator, runner_args, job_args)

def main():
    args = sys.argv
    StatisticsGenerator.generate_stats(args)

if __name__ == '__main__':
    main()

