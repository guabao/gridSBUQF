__doc__ = "useful array supply function."

import numpy

def mv(A, b):
# vector b multiplied by a matrix A, return c = Ab
    assert len(A.shape) == 2, "A must be a matrix!"
    assert (len(b.shape) == 1) or ((len(b.shape) == 2) and (b.shape[-1] == 1)), "b must be a vector or vector-like matrix!"
    b1 = b.ravel()
    assert A.shape[1] == b1.shape[0], "A and b must have same dimension!"
    return numpy.dot(A, b.ravel())


def vm(b, A):
    return mv(A.T, b)


def mm(A, B):
# matrix B multiplied by a matrix A, reutrn C = AB
    assert len(A.shape) == 2, "A must be a matrix!"
    assert len(B.shape) == 2, "B must be a matrix!"
    assert A.shape[1] == B.shape[0], "A and B must have same dimension!"
    return numpy.dot(A, B)


def isin(A, B):
    # given two arrays/lists A and B return an array whether the element of A is in B or not
    # future work: make a C version of this function
    if hasattr(B, '__len__'):
        B1 = numpy.sort(numpy.array(B))
    else:
        B1 = numpy.sort(numpy.array([B]))
    if hasattr(A, '__len__'):
        A1 = numpy.sort(numpy.array(A))
    else:
        A1 = numpy.sort(numpy.array([A]))
    flag = numpy.empty(A1.shape)
    i = 0
    j = 0
    lenA = A1.shape[0]
    maxB = B1.shape[0] - 1
    while (i < lenA):
        if A1[i] < B1[j]:
            flag[i] = False
        elif A1[i] == B1[j]:
            flag[i] = True
            j += 1
        else:
            j += 1
        i += 1
        j = min(j, maxB)
    return flag.astype(bool)


def intersect(ar1, ar2, assume_unique=False):
    '''call numpy.intersect1d'''
    return numpy.intersect1d(ar1, ar2, assume_unique=False)


def unique(arr):
    # a smart function test unique
    if isinstance(arr, numpy.ndarray):
        return numpy.unique(arr)
    else:
        return list(sorted(set))


def setnull(arr, val):
    return numpy.where(numpy.isfinite(arr), arr, val)
