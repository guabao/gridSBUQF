__doc__ = 'second version of grid framework'
import numpy
import datetime
import copy
import os
from util import arr

import pdb
class grid():
	# on-going grid class
	def __init__(self, data, name=None, dtm=None, fields=None):
	# First suppose data is a list of two dimensional arrays corresponding to fields
		assert len(data) == len(fields), 'Invalid data!'
		for datafield in data:
			assert len(dtm) == len(datafield[:,0]), 'Data should have same raw length as datetime!'
			assert len(name) == len(datafield[0,:]), 'Data should have same column length as name!'
		self.data = {k:v for k,v in zip(fields, data)}
		self.dtm = numpy.array(dtm)
		self.name = numpy.array(name)
		self.fields = numpy.array(fields)
		self.__nameSorted__ = False
		self.__dtmSorted__ = False
		return None
		
	def __repr__(self):
		return str(self.data)
		
	def __getitem__(self, *args):
		if not isinstance(args[0], tuple):
			subdtm = args[0]
			subname = self.name
			subfields = self.fields
			subdata = [self.data[k][subdtm,:] for k in self.data]
		elif len(args[0]) == 2:
			subdtm = args[0][0]
			subname = args[0][1]
			subfields = self.fields
			subdata = [self.data[k][subdtm,arr.isin(self.name,subname)] for k in self.data]
		else:
			raise Exception("Invalid slicing!")
		return grid(subdata, subname, subdtm, subfields)
		
		
	def addFields(self, data, dtm=None, name=None, fields=None):
		assert not fields is None, 'Invalid fields!'		
		assert len(data) == len(fields), 'Invalid data!'
		for datafield in data:
			assert len(self.dtm) == len(datafield[:,0]), 'Data should have same raw length as original!'
			assert len(self.name) == len(datafield[0,:]), 'Data should have same column length as original!'
		self.fields = numpy.concatenate((self.fields,fields))
		self.data.update({k:v for k,v in zip(fields,data)})
		return None
	
	def sortDtm(self):
		for field in self.fields:
			self.data[field] = self.data[field][numpy.argsort(self.dtm),:]
		self.dtm = numpy.sort(self.dtm)
		self.__dtmSorted__ = True
		return None
		
	def sortName(self):
		for field in self.fields:
			self.data[field] = self.data[field][:,numpy.argsort(self.name)]
		self.name = numpy.sort(self.name)
		self.__nameSorted__ = True
		return None
	
	
	def save(self, path):
		saveGrid(self, path)
		return None
		
		
def saveGrid(grid, path):
	# save to a folder
	if not os.path.exists(path):
		os.makedirs(path)
	numpy.save(path+'\\name', grid.name)
	numpy.save(path+'\\dtm', grid.dtm)
	numpy.save(path+'\\fields', grid.fields)
	if not os.path.exists(path+'\\fields'):
		os.makedirs(path+'\\fields')
	for field in grid.fields:
		numpy.save(path+'\\fields\\'+field, grid.data[field])
	return None
	
def loadGrid(path):
	# load from a folder
	name = numpy.load(path+'\\name.npy')
	fields = numpy.load(path+'\\fields.npy')
	dtm = numpy.load(path+'\\dtm.npy')
	data = []
	for field in fields:
		data.append(numpy.load(path+'\\fields\\'+field+'.npy'))
	return grid(data, name, dtm, fields)
		
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
	dtm = [10,9,8,7,6,5,4,3,2,1]
	name = ['d','b','c']
	fields = ['open','close']
	g = grid(data,name,dtm,fields)
	return g
	
def demo_addFields():
	data = [numpy.random.rand(10,3), numpy.random.rand(10,3)]
	fields = ['high','low']
	return fields, data