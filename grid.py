__doc__ = 'basic grid class'
__author__ = 'Jiazhou Wang'
__version__ = '0.1a'
__date__ = '2019-06-07'


import copy
import pandas
import numpy
import datetime

# gridSBUQF related
from util import arr

import pdb


class gridDense(object):
    '''
    Dense grid object.
    '''
    def __init__(self, data, dtm=None, name=None, field=None, is_sorted=True):
        # check data
        if isinstance(data, numpy.ndarray):
            if len(data.shape) == 2:
                assert len(dtm) == data.shape[0], 'Data should have same row length as datetime!'
                assert len(name) == data.shape[1], 'Data should have same column lenght as name!'
                # create object
                self._data = {field: data}
                self.dtm = arr.array(dtm)
                self.name = arr.array(name)
                self.field = arr.array([field])
            elif len(data.shape) == 3:
                assert len(field) == data.shape[0], 'Data should have same length as field!'
                assert len(dtm) == data.shape[1], 'Data should have same row length as datetime!'
                assert len(name) == data.shape[2], 'Data should have same column lenght as name!'
                # create object
                self._data = {fi:datai for fi, datai in zip(field, data)}
                self.dtm = arr.array(dtm)
                self.name = arr.array(name)
                self.field = arr.array(field)
            else:
                raise NotImplementedError('Invalid input!')
        else:
            raise NotImplementedError('Data should have type as numpy.ndarray!')
        self.is_sorted = False
        if is_sorted:
            self.sort()

        # freeze the object
        self.__freeze__ = True
        return None

    # support functions
    def sort(self, force=False):
        '''
        Sort dtm, name.
        '''
        # Go through the logic if this grid needs a sort process.
        if not force:
            if self.is_sorted:
                return
        idx_dtm = numpy.argsort(self.dtm)
        idx_name = numpy.argsort(self.name)
        self.dtm = self.dtm[idx_dtm]
        self.name = self.name[idx_name]
        for fi in self.field:
            self.field[fi] = self.field[fi][idx_dtm, :][:, idx_name]
        self.is_sorted = True
        return None

    def merge_dtm_hard(self, g_new):
        '''
        Append new grid to current grid on dtm.
        Hard merge means fields and names should be exactly same.
        '''
        assert numpy.all(g_new.field == self.field), 'The grid should have same fields!'
        assert numpy.all(g_new.name == self.name), 'The grid should have same names!'
        self.is_sorted = False
        self.dtm = numpy.append(self.dtm, g_new.name)
        for fi in self.field:
            self.field[fi] = numpy.append(self.field[fi], g_new.field[fi], axis=0)
        self.sort()
        return None

    def merge_name(self, g_new):
        '''
        Append new grid to current grid on name.
        Hard merge means fields and dtms should be exactly same.
        '''
        assert numpy.all(g_new.field == self.field), 'The grid should have same fields!'
        assert numpy.all(g_new.dtm == self.dtm), 'The grid should have same dtms!'
        self.is_sorted = False
        self.name = numpy.append(self.name, g_new.name)
        for fi in self.field:
            self.field[fi] = numpy.append(self.field[fi], g_new.field[fi], axis=1)
        self.sort()
        return None

    def append_field(self, g_new):
        '''
        Append new grid to current grid on name.
        Hard merge means fields and dtms should be exactly same.
        '''
        assert numpy.all(g_new.name == self.name), 'The grid should have same names!'
        assert numpy.all(g_new.dtm == self.dtm), 'The grid should have same dtms!'
        overlap = numpy.isin(g_new.field, self.field)
        if numpy.any(overlap):
            raise AssertionError("The grid has overlapped field on %s"%', '.join\
                                 (g_new.field[overlap]))
        for fi in g_new.field:
            self.field[fi] = g_new.field[fi]
        return None


def _test_gridDense():
    '''
    Test function for grid dense.
    '''
    dtms = numpy.arange('2019-01-01', '2019-06-01', dtype='datetime64')
    names = numpy.array('AAPL MSFT'.split())
    data_open = numpy.random.rand(len(dtms), len(names))
    data_close = numpy.random.rand(len(dtms), len(names))
    g = gridDense(numpy.array([data_open, data_close]), dtm=dtms, name=names, field='Open CLose'.split())
    return g
