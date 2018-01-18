__doc__ = '''cache module'''

import sys

import numpy

GLOBALS_VALS = []
GLOBALS_NUM = 10
GLOBALS_HASHS = numpy.zeros(GLOBALS_NUM+1)


def cacheMemory(func):
    def func_wrapper(*args):
        global_val = sys.modules[func.__module__].cache.GLOBALS_VALS
        global_num = sys.modules[func.__module__].cache.GLOBALS_NUM
        global_hash = sys.modules[func.__module__].cache.GLOBALS_HASHS
        func_hash = func.__hash__()
        flag = global_hash == func_hash
        if numpy.any(flag):
            return global_val[numpy.argwhere(flag).ravel() - 1]
        else:
            result = func(*args)
            if len(global_val) == global_num:
                temp = global_val[1:]
                global_val = temp
                global_hash[:-1] = global_hash[1:]
            global_val += [result]
            global_hash[len(global_val)] = func_hash
            return result
    return func_wrapper




