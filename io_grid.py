__doc__ = 'io module'
__author__ = 'jiazhou wang'
__date__ = '05/02/2017'

__requirement__ = r'''

pytables

'''


import pandas
import grid


def save_grid(g, path):
    # save a grid type to disk 
    assert isinstance(g, grid.gridOneField), 'Input should be grid type!'
    g.pandasFrame.to_hdf(path, 'table', append = True)
    return None


def load_grid(path):
    store = pandas.HDFStore(path)
    g = store['table']
    store.close()
    return g


def save_grid_sparse(g, path):
    # save a sparse grid object to disk, will append in save_grid()
    return None


def load_grid_sparse(path):
    # load a sparse grid object from disk, will append in load_grid()
    return None



def grid2mat(g):
    # given a grid object, transfer data to matlab matrix object
    return mx


def mat2grid(mx, axis = None):
    # transfer a matlab maxtrix object to grid object
    return g


def grid2R_object(g):
    # transfer grid object to an object in R
    return None


def R_object2grid():
    # transfer a R object to grid
    return None
