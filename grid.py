__doc__ = 'basic grid class'
__author__ = 'Jiazhou Wang'
__version__ = '0.1a'

import pandas
import numpy
import datetime


class gridOneField():
    '''grid class based on pandas'''
    def __init__(self, data, dtm, name, field):
        #check data
        assert isinstance(data, numpy.ndarray), 'Data type should be numpy array!'
        assert len(data.shape) == 2, 'Data should be two dimension array!'
        assert len(dtm) == len(data[:, 0]), 'Data should have same raw length as datetime!'
        assert len(name) == len(data[0, :]), 'Data should have same column length as name!'
    
        #create object
        multipleIndex = pandas.MultiIndex.from_product([dtm, name], names = ['dte', 'name'])
        self.pandasFrame = pandas.DataFrame(data.ravel(), index = multipleIndex, columns = [field])
        self.dtm = numpy.array(dtm)
        self.name = numpy.array(name)
        self.fields = self.pandasFrame.columns
        return None
    

    def append(self, data, dtm=None, name=None, field=None):
        assert not field is None, 'Invalid field!'
        if dtm is None:
            assert data.shape[0] == self.dtm.shape[0], 'Invalid datetime length!'
        else:
            #raise Exception('Under Construction!')
            raise NotImplementedError('Under Construction!')
            assert data.shape[0] == len(dtm), 'Invalid datetime length!'
        if name is None:
            assert data.shape[1] == self.name.shape[0], 'Invalid name length!'
        else:
            raise NotImplementedError('Under Construction!')
            assert data.shape[1] == len(name), 'Invalid name length!'
        self.pandasFrame = self.pandasFrame.assign(**{field: data.ravel()})
        self.fields = self.pandasFrame.columns
        return None


    def select(self, days, names):
        return None

    

