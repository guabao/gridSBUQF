__doc__ = 'basic grid class'
__author__ = 'Jiazhou Wang'
__version__ = '0.1a'


import copy
import pandas
import numpy
import datetime

# gridSBUQF related
import io_grid
from util import arr

import pdb


__inputShape__ = ['data', 'datetime', 'name', 'columns']


class gridDense():
    '''grid class based on pandas'''
    def __init__(self, data, dtm=None, name=None, field=None):
        #check data
        if isinstance(data, numpy.ndarray):
            assert len(data.shape) <= 3, 'Data should be two dimension array!'
            if len(data.shape) == 2:
                assert len(dtm) == len(data[:, 0]), 'Data should have same raw length as datetime!'
                assert len(name) == len(data[0, :]), 'Data should have same column length as name!'

                #create object
                multipleIndex = pandas.MultiIndex.from_product([dtm, name], names = ['dte', 'name'])
                self.pandasFrame = pandas.DataFrame(data.ravel(), index = multipleIndex, columns = field if isinstance(field, list) else [field])
            elif len(data.shape) == 3:
                assert data.shape[2] == len(field), 'Invalid Field Input!'
                multipleIndex = pandas.MultiIndex.from_product([dtm, name], names = ['dte', 'name'])
                self.pandasFrame = pandas.DataFrame(data[:, :, 0].ravel(), index = multipleIndex, columns = [field[0]])
                self.pandasFrame = self.pandasFrame.assign(**{field[i]:data[:, :, i].ravel() for i in xrange(1, len(field))})
            else:
                raise NotImplementedError('Under Construction!')
        elif isinstance(data, pandas.core.frame.DataFrame):
            self.pandasFrame = data
            dtm = data.index.get_level_values(0)
            name = numpy.unique(data.index.get_level_values(1))
        else:
            raise NotImplementedError('Invalid Data Frame!')
        self.dtm = numpy.array(dtm)
        self.name = numpy.array(name)
        self.fields = self.pandasFrame.columns
        self.shape = (len(self.dtm), len(self.name), len(self.fields))
        self.__inputShape__ = __inputShape__
        return None
    

    def append(self, data, dtm=None, name=None, field=None):
        assert not field is None, 'Invalid field!'
        if dtm is None:
            assert data.shape[0] == self.dtm.shape[0], 'Invalid datetime length!'
        else:
            #raise Exception('Under Construction!')
            #raise NotImplementedError('Under Construction!')
            assert data.shape[0] == len(dtm), 'Invalid datetime length!'
        if name is None:
            assert data.shape[1] == self.name.shape[0], 'Invalid name length!'
        else:
            #raise NotImplementedError('Under Construction!')
            assert data.shape[1] == len(name), 'Invalid name length!'
        self.pandasFrame = self.pandasFrame.assign(**{field: data.ravel()})
        self.fields = self.pandasFrame.columns
        return None


    def select(self, dtm, name=None):
        # dimension selection
        mx = self.pandasFrame.values
        if name is None:
            name = self.name
        return gridDense(mx.reshape(self.shape)[arr.isin(self.dtm, dtm), :][:, arr.isin(self.name, name)], dtm=dtm, name=name, field=self.fields)
    
    
    def sparse(self):
        # transfer current grid to a sparse grid object
        return None
    
    
    def dense(self):
        # transfer a sparse grid object to dense grid object
        return None
    

    def save(self, path):
        io_grid.save_grid(self, path)
        print 'SAVED!'
        return None

    
    def sparse_rate(self):
        # compute the percentage of non zero data
        return None

    # print related
    def __repr__(self):
        return str(self.pandasFrame)

    def __getitem__(self, *args):
        if len(args[0]) == 1:
            subdtm = self.dtm[args[0]]
            subname = self.name[slice(None, None, None)]
        elif len(args[0]) == 2:
            subdtm = self.dtm[args[0][0]]
            subname = self.name[args[0][1]]
        else:
            raise Exception("Invalid slicing!")
        #pdb.set_trace()
        return self.select(subdtm, subname)


class gridSparse():
    '''sparse grid object'''
    def __init__(slef):
        return None
    
    
def merge(gs):
    g1 = copy.deepcopy(gs[0])
    dtm = gs[0].dtm
    assert numpy.all([numpy.all(gi.dtm == dtm) for gi in gs[1:]]), 'Grids being merged should have same dtms.'
    # to do: support multiple fields
    assert numpy.all([len(gi.fields) for gi in gs]), 'Only support one field!'
    for gi in gs[1:]:
        g1.append(data=gi.pandasFrame.values, dtm=gi.dtm, name=g1.name, field=gi.fields[0])
        pass
        #g1.append(
    # merge a list of dense/sparse grid object
    return g1


def pandas2grid(pandas_obj):
    # create a grid object from pandas dataFrame object
    return None
