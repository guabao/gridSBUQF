#!/usr/bin/env python
# -*- coding: utf-8 -*-
__doc__ = 'data loader module for NYSE TAQ data.'
__author__ = 'Jiazhou Wang'
__date__ = 'May 05, 2019'


import numpy
import gzip
import os

class DataLoader(object):
    '''
    DataLoader module for NYSE TAQ data
    Currently not used
    '''


def process_data_gzip(file_path):
    '''
    Process data from NYSE TAQ gzip file
    '''
    # Validate the file path
    if not os.path.isfile(file_path):
        raise IOError('No file is found in file_path: %s'%file_path)

    mx = []

    return None


