__doc__ = "some useful functions."

def check_mkl(n):
# if using mkl then set the num of threads to n
    import numpy
    if numpy.__config__.lapack_mkl_info:
        import ctypes
        mkl_rt = ctypes.CDLL('libmkl_rt.so')
        mkl_rt.mkl_set_num_threads(ctypes.byref(ctypes.c_int(n)))
        print "set mkl num threads to %i"%(n)
    else:
        print "no mkl linked to python!"
    return None
