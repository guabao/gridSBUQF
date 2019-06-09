__doc__ = 'io module'
__author__ = 'jiazhou wang'
__date__ = '06/08/2019'

import os

import numpy

import grid


def save_grid(g, path):
    '''
    Save a grid type object to disk
    '''
    # check the existence of the directory
    if os.path.isfile(path) or os.path.isdir(path):
        raise AssertionError('File/Directory is already existed.')

    os.mkdir(path)
    path = path if path[-1] == '/' else path + '/'

    # save data
    numpy.save(path + 'dtm.npy', g.dtm)
    numpy.save(path + 'name.npy', g.name)
    numpy.save(path + 'field.npy', g.field)
    for fi in g.field:
        numpy.save(path + str(fi) + '.npy', fi)

    print("DONE!")
    return None


def load_grid(g, path):
    '''
    Load a grid type object from disk
    '''
    # check the existence of the directory
    assert os.path.isdir(path), 'File does not exist!'
    path = path if path[-1] == '/' else path + '/'
    dtm = numpy.load(path + 'dtm.npy')
    name = numpy.load(path + 'name.npy')
    field = numpy.load(path + 'field.npy')
    data = []
    for fi in field:
        data += numpy.load(path + fi + '.npy')
    return grid.gridDense(numpy.array(data), dtm, name, field, is_sorted=True)

