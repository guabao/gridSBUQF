__doc__ = 'test code'

import numpy
import pandas


import grid


def tutorial():
    'test grid creation'

    mx = numpy.random.rand(10, 4)
    dte = pandas.date_range('20130101', periods = 10)
    g = grid.gridOneField(mx, dte, list('ABCD'), 'ask')
    mx1 = numpy.random.rand(10, 4)
    g.append(mx1, field = 'bid')
    return g
