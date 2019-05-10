#!/usr/bin/env python
# -*- coding: utf-8 -*-
__doc__ = 'Name module for NYSE TAQ data.'
__author__ = 'Jiazhou Wang'
__date__ = 'May 05, 2019'

import os
import numpy


class Names():
    '''
    This class is a hard coded name class for US market
    The rule is select the names who has top 3000 daily trading volumes
    '''



def _process_txt_2_csv():
    folder = os.getcwd()
    file_names = os.listdir(folder)
    file_avail = list(filter(lambda x: x if '.txt' in x else None, file_names))
    for fi in file_avail:
        print(fi)
        with open(fi, 'r') as f:
            s = numpy.array(eval(f.read()))
            numpy.savetxt(fi[:-4]+'.csv', s, fmt='%s', delimiter=',')
    print('DONE!')
    return None


def load_names(year, region='US'):
    '''
    Load names from txt file
    '''
    
    assert region is 'US', 'Only support US region!'
    assert type(year) is int, 'Year should be an integer!'

    path = os.getcwd()
    file_path = None
    return None
