'''
Created on Jan 24, 2014

@author: himanshu
'''
import csv
import argparse

class Utils:
    @classmethod
    def get_data_vectors(cls, data_file, delimiter):
        with open(data_file, 'r') as file:
            data_reader = csv.reader(file, delimiter = delimiter)
            for row in data_reader:
                yield row
