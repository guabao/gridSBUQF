__doc__ = 'basic grid class'

import pandas
import numpy
import datetime


class gridSBUQF():
    '''grid class based on pandas'''
    def __init__(self, data, dtm, name):
        'check data'
        assert isinstance(data, numpy.ndarray), 'Data type should be numpy array!'
        assert len(data.shape) == 2, 'Data should be two dimension array!'
        assert len(dtm) == len(data[:, 0]), 'Data should have same raw length as datetime!'
        assert len(name) == len(data[0, :]), 'Data should have same column length as name!'
        
        'create object'
        self.pandasFrame = pandas.DataFrame(data, index = dtm, columns = name)
        return None
