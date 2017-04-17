__doc__ = 'test code'

import numpy
import pandas


import grid


def test_grid():
    'test grid creation'

    mx = numpy.random.rand(10, 4)
    dte = pandas.date_range('20130101', periods = 10)
    g = grid.gridOneField(mx, dte, list('ABCD'), 'price')
    return g
