__doc__ = 'second version of grid framework'


import numpy


class grid():
    # on-going grid class
    def __init__(self, data, name=None, dtm=None, field=None):
        # First suppose data is a list of two dimensional arrays corresponding to fields
        assert len(data) == len(field), 'Invalid data!'
        return None
