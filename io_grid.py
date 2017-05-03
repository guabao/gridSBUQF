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
    return store['table']
