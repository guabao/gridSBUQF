__doc__ = 'Framework of back test.'

# built-in module
import datetime

# numpy scipy related
import numpy

# in-house related
import grid_v2


def backTestCore(dtms, fUniverse, fRetrivePos, fOptimization, fTcost):

    #   back test frame work
    #
    #   description of inputs:
    #
    #   dtms        :   1 dimension numpy array indicating the datetime range in the simulation
    #   fUniverse   :   a function returns a 1 dimension numpy array including the trading universe for the input dtm
    #   fRetrivePos :   a function returns pre-position given dtm, name, and position grid
    #   fOptimization:  a function returns the target position given position grid
    #   fTcost      :   a function returns the transaction cost paid given the position

    #initialization

    name_all = union([fUniverse(dtmi) for dtmi in dtms])    # get all the names
    pos = pos_init(dtms, name_all)                          # initialize back test position
    
    for i, dtmi in enumerate(dtms):
        
        name_active = fUniverse(dtmi)

        pre_pos = fRetrivePos(dtmi, name_active, pos)

        order = fOptimization(dtmi, name_active, pre_pos)

        pos = fUpdateOrder(pos, order, fTcost)

    return pos


def _posInit(dtm, name):
    n = dtm.shape[0]
    m = name.shape[0]
    fields = 'dPrePos uPrePos dTrade uTrade dTargetPos uTargetPos dCumCash dCumTcost'.split()
    data = [numpy.zeros((n, m)) for fi in fields]
    return grid_v2.grid(data, name, dtm, fields)

def _testPosInit():
    n = 10
    m = 5
    name = numpy.array('a b c d e'.split())
    dtms = numpy.array([datetime.datetime.now() + datetime.timedelta(minutes=5*i) for i in xrange(n)])
    return _posInit(dtms, name)


def _testOpt(fPrice):
    def fOpt(dtm, names, pre_pos):
        dtm = numpy.array(dtm)
        position = numpy.random.rand(1, len(names))
        gPrice = fPrice(dtm, names)
        trade = 1. * (position - pre_pos) / gPrice.data['price']
    return grid_v2.grid(trade[None, :], dtm, names, ['order'])
