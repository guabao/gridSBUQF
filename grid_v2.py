__doc__ = 'second version of grid framework'
import numpy
import datetime
import copy
import os
from util import arr

import pandas

import pdb

class grid():
    # on-going grid class
    def __init__(self, data, dtm=None, name=None, fields=None):
	# First suppose data is a list of two dimensional arrays corresponding to fields
        assert len(data) == len(fields), 'Invalid data!'
        #assert isinstance(dtm, numpy.ndarray) or isinstance(dtm, pandas.tseries.index.DatetimeIndex), 'Invalid dtm type'
        assert isinstance(dtm, numpy.ndarray), 'Invalid dtm type'
        assert isinstance(name, numpy.ndarray), 'name should be numpy.ndarray type'
        for datafield in data:
            assert dtm.shape[0] == datafield.shape[0], 'Data should have same raw length as original!'
            assert name.shape[0] == datafield.shape[1], 'Data should have same column length as original!'
        self.data = {k:v for k,v in zip(fields, data)}
        self.dtm = numpy.array(dtm)
        self.name = numpy.array(name)
        self.fields = numpy.array(fields)
        self.shape = data[0].shape
        self.__nameSorted__ = False
        self.__dtmSorted__ = False
        return None

    def __repr__(self):
        return str(self.data)
        
    def __len__(self):
        return self.shape[0]

    def __getitem__(self, *args):
        if not isinstance(args[0], tuple):
            indexDtm = args[0]
            indexName = slice(None, None, None)
        elif len(args[0]) == 2:
            indexDtm = args[0][0]
            indexName = args[0][1]
        else:
            raise Exception("Invalid slicing!")
        subData = [self.data[k][indexDtm][indexName] for k in self.data]
        return grid(subData, self.dtm[indexDtm], self.name[indexName], self.fields)


    def select(self, dtm, name):
        self.sortDtm()
        self.sortName()
        if numpy.any(dtm[:-1] < dtm[1:]):
            dtm.sort()
        if numpy.any(name[:-1] < name[1:]):
            name.sort()
        shape = [dtm.shape[0], name.shape[0]] 
        mx0 = numpy.empty(shape)
        mx0[:] = numpy.nan
        gg = grid([mx0.copy() for _ in self.fields], dtm, name, self.fields)
        #dtmCommon, dtmFlag1, dtmFlag2 = arr.intersect(self.dtm, dtm, flag1 = True, flag2 = True)
        dtmCommon = numpy.intersect1d(self.dtm, dtm)
        dtmFlag1 = arr.isin(dtm, dtmCommon)
        dtmFlag2 = arr.isin(self.dtm, dtmCommon)
        nameCommon = numpy.intersect1d(self.name, name)
        nameFlag1 = arr.isin(name, nameCommon)
        nameFlag2 = arr.isin(self.name, nameCommon)
        #nameCommon, nameFlag1, nameFlag2 = arr.intersect(self.name, name, flag1 = True, flag2 = True)
        flag1 = dtmFlag1[:, None] * nameFlag1[None, :]
        flag2 = dtmFlag2[:, None] * nameFlag2[None, :]
        for fi in self.fields:
            gg.data[fi][flag1] = self.data[fi][flag2]
        return gg
		
		
    def addFields(self, data, dtm=None, name=None, fields=None):
        assert not fields is None, 'Invalid fields!'		
        assert len(data) == len(fields), 'Invalid data!'
        for datafield in data:
            assert self.dtm.shape[0] == datafield.shape[0], 'Data should have same raw length as original!'
            assert self.name.shape[0] == datafield.shape[1], 'Data should have same column length as original!'
        self.fields = numpy.concatenate((self.fields,fields))
        self.data.update({k:v for k,v in zip(fields,data)})
        return None

    def sortDtm(self):
        if self.__dtmSorted__ is False:
            for field in self.fields:
                self.data[field] = self.data[field][numpy.argsort(self.dtm),:]
        #self.dtm = numpy.sort(self.dtm)
        self.dtm.sort()
        self.__dtmSorted__ = True
        return None

    def sortName(self):
        if self.__nameSorted__ is False:
            for field in self.fields:
                self.data[field] = self.data[field][:,numpy.argsort(self.name)]
        #self.name = numpy.sort(self.name)
        self.name.sort()
        self.__nameSorted__ = True
        return None


    def save(self, path):
        saveGrid(self, path)
        return None


def saveGrid(grid, path):
    # save to a folder
    if not os.path.exists(path):
        os.makedirs(path)
    numpy.save(path+'/name', grid.name)
    numpy.save(path+'/dtm', grid.dtm)
    numpy.save(path+'/fields', grid.fields)
    if not os.path.exists(path+'/fields'):
        os.makedirs(path+'/fields')
    for field in grid.fields:
        numpy.save(path+'/fields/'+field, grid.data[field])
    return None

def loadGrid(path):
	# load from a folder
	name = numpy.load(path+'/name.npy')
	fields = numpy.load(path+'/fields.npy')
	dtm = numpy.load(path+'/dtm.npy')
	data = []
	for field in fields:
		data.append(numpy.load(path+'/fields/'+field+'.npy'))
	return grid(data, dtm, name, fields)
		
def hstack(grids):
	assert len(grids) > 1, 'Grids should be a list length greater than 1!'		
	g = copy.deepcopy(grids[0])
	fields = g.fields		
	dtm = g.dtm
	assert numpy.all([set(grid.dtm) == set(dtm) for grid in grids]), 'Grids being merged should have same dtms!'
	assert numpy.all([set(grid.fields) == set(fields) for grid in grids]), 'Grids being merged should have same fields!'
	
	for grid in grids[1:]:
		g.name = numpy.concatenate((g.name,grid.name))
		for f in fields:
			g.data[f] = numpy.hstack((g.data[f],grid.data[f]))
	g.__nameSorted__ = False	
	return g
		
def vstack(grids):
	assert len(grids) > 1, 'Grids should be a list length greater than 1!'
	g = copy.deepcopy(grids[0])
	fields = g.fields
	name = g.name
	assert numpy.all([set(grid.fields) == set(fields) for grid in grids]), 'Grids being merged should have same fields!'
	assert numpy.all([set(grid.name) == set(name) for grid in grids]), 'Grids being merged should have same names!'
	
	for grid in grids[1:]:
		g.dtm = numpy.concatenate((g.dtm,grid.dtm))
		for f in fields:
			g.data[f] = numpy.vstack((g.data[f],grid.data[f]))
	g.__dtmSorted__ = False
	return g
			

def demo():
	data = [numpy.random.rand(10,3), numpy.random.rand(10,3)]
	dtm = numpy.array([10,9,8,7,6,5,4,3,2,1])
	name = numpy.array(['d','b','c'])
	fields = ['open','close']
	g = grid(data,dtm,name,fields)
	return g
	
def demo_addFields():
	data = [numpy.random.rand(10,3), numpy.random.rand(10,3)]
	fields = ['high','low']
	return fields, data
