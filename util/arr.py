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
