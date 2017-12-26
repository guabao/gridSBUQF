__doc__ = 'second version of grid framework'
import numpy
import datetime
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
		self.fields = fields
		#self.nameDict = {k:v for k,v in zip(name,range(len(name)))}
		return None
		
	def __repr__(self):
		return str(self.data)
		
	def __getitem__(self, *args):
		if len(args[0]) == 1:
			subdtm = args[0][0]
			subname = self.name
			subfields = self.fields
			#subdata = {k:self.data[k][subdtm,:] for k in self.data}
			subdata = [self.data[k][subdtm,:] for k in self.data]
		elif len(args[0]) == 2:
			subdtm = args[0][0]
			subname = args[0][1]
			subfields = self.fields
			#subdata = {k:self.data[k][subdtm,subname] for k in self.data}
			subdata = [self.data[k][subdtm,arr.isin(self.name,subname)] for k in self.data]
		else:
			raise Exception("Invalid slicing!")
		pdb.set_trace()
		return grid(subdata, subname, subdtm, subfields)
		
	def argtest(self,*args):
		pdb.set_trace()
		

def demo():
	data = [numpy.random.rand(10,3), numpy.random.rand(10,3)]
	dtm = list(range(10))
	name = ['a','b','c']
	fields = ['open','close']
	g = grid(data,name,dtm,fields)
	return g