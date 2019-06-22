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

        # set attribute for each field
        for fi in field:
            setattr(self, fi, self._data[fi])

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
            self._data[fi] = self._data[fi][idx_dtm, :][:, idx_name]
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

    def project(self, dtm, name, field, none_value=numpy.nan):
        '''
        Project current grid to a set of (field, dtm, name).
        A rough project means the new tuple of (field, dtm, name) should be a
        strict subset of the tuple of original grid.
        '''
        #flag_dtm = numpy.isin(self.dtm, dtm)
        #flag_name = numpy.isin(self.name, name)
        field = numpy.array(field)
        if not field.shape:
            field = field.reshape([1])
        flag_field = numpy.isin(field, self.field)

        #assert len(dtm) == numpy.sum(flag_dtm), 'The input dtm should be a strict subset of dtms of the grid!'
        #assert len(name) == numpy.sum(flag_name), 'The input name should be a strict subset of names of the grid!'
        assert numpy.all(flag_field), 'The input field should be a subset of fields of the grid!'

        data = []
        for fi in field:
            data_fi = numpy.empty([len(dtm), len(name)])
            data_fi[:] = none_value
            idx_dtm1, idx_dtm2 = numpy.where(dtm[:, None] == self.dtm[None, :])
            idx_name1, idx_name2 = numpy.where(name[:, None] == self.name[None, :])
            data_fi[idx_dtm1[:, None], idx_name1[None, :]] = self._data[fi][idx_dtm2[:, None], \
                                                                            idx_name2[None, :]]
            data.append(data_fi)
        return gridDense(numpy.array(data), dtm, name, field)


def _test_gridDense():
    '''
    Test function for grid dense.
    '''
    dtms = numpy.arange('2019-01-01', '2019-06-01', dtype='datetime64')
    names = numpy.array('AAPL MSFT'.split())
    data_open = numpy.random.rand(len(dtms), len(names))
    data_close = numpy.random.rand(len(dtms), len(names))
    g = gridDense(numpy.array([data_open, data_close]), dtm=dtms, name=names, field='Open Close'.split())
    return g
