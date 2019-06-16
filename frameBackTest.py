__doc__ = 'Framework of back test.'

# built-in module
import datetime

# numpy scipy related
import numpy

# in-house related
#import grid_v2
import grid
from util import arr, cal

# debug
import pdb


def backTestCore(dtms, fUniverse, fPrice, fRetrievePos, fOptimization, fUpdateOrder, fTcost):

    '''
    #   back test frame work
    #
    #   description of inputs:
    #
    #   dtms        :   1 dimension numpy array indicating the datetime range in the simulation
    #   fUniverse   :   a function returns a 1 dimension numpy array including the trading universe for the input dtm
    #   fPrice      :   a function returns the prices of current name given dtm and name
    #   fRetrivePos :   a function returns pre-position given dtm, name, and position grid
    #   fOptimization:  a function returns the target position given position grid
    #   fUpdateOrder:   a function returns the simulation gride after fill
    #   fTcost      :   a function returns the transaction cost paid given the position
    '''

    #initialization

    name_all = numpy.unique(numpy.concatenate([fUniverse(dtmi) for dtmi in dtms]))    # get all the names
    #pdb.set_trace()
    pos = _posInit(dtms, name_all)                          # initialize back test position
    
    for i, dtmi in enumerate(dtms):
        
        print('------ %s ------ running simulation on %s ------'%(str(datetime.datetime.now()),str(dtmi)))

        dtmi = arr.array(dtmi)
        
        name_active = fUniverse(dtmi)

        pre_pos = fRetrievePos(dtmi, name_active, fPrice, pos)

        order = fOptimization(dtmi, name_active, fPrice, pre_pos)

        pos = fUpdateOrder(pos, order, fPrice, fTcost)

    return pos


def _posInit(dtm, name):
    n = dtm.shape[0]
    m = name.shape[0]
    fields = 'dPrePos uPrePos dTrade uTrade dTargetPos uTargetPos dCash dTcost'.split()
    data = numpy.array([numpy.zeros((n, m)) for fi in fields])
    g = grid.gridDense(data, dtm, name, fields)
    return g

def _testPosInit():
    n = 10
    m = 5
    name = numpy.array('a b c d e'.split())
    dtms = numpy.array([numpy.datetime64(datetime.datetime.now()) + numpy.timedelta64(5*i, 'm') for i in range(n)])
    return _posInit(dtms, name)



def _retrievePos(dtm, name, pos):
    '''
    given a grid ovject pos, target dtm and name
    return the current dollar position
    '''
    return pos.data['dPrePos'][arr.isin(pos.dtm, dtm), arr.isin(pos.name, name)]


def _tcost(dtm, name):
    '''
    given target dtm and name,
    return a grid with expected transaction costs
    '''
    return None


def _priceETH():
    '''
    ETH price grid
    '''
    g = numpy.load('ETHData.csv.npy')
    dtm = numpy.array(map(datetime.datetime.fromtimestamp, g[0])).astype('datetime64[ms]')
    price = g[1]
    name = numpy.array(['ETHUSD'])
    return grid_v2.grid([price[:, None]], dtm, name, ['price'])


def _ETHOpt(fPrice):
    def fOpt(dtm, names, pre_pos):
        dtm = arr.array(dtm)
        position = numpy.random.rand(1, len(names))
        gPrice = fPrice(dtm, names)
        trade = 1. * (position - pre_pos) / gPrice.data['price']
        return grid_v2.grid([trade], dtm, names, ['order'])
    return fOpt


def _testOpt():
    g = _priceETH()
    return _ETHOpt(g.select)


def _fixTcost(fprice, bps):
    '''
    fix tcost function with given basis points
    '''
    def ftcost(dtm, name):
        price = fprice(dtm, name).data['price']
        return price * bps
    return ftcost


def _fixTcost5Bps():
    '''
    fix tcost function, value = 5bps
    '''
    return _fixTcost(_priceETH().select, 5e-4)


def _updateOrder(fPrice):
    '''
    sample update order function
    '''
    def f(pos, order, fTcost):
    #pdb.set_trace()
        flagDtm = arr.isin(pos.dtm, order.dtm)
        flagName = arr.isin(pos.name, order.name)
        pos.data['uTrade'][flagDtm, flagName] = order.data['order']
        price = fPrice(order.dtm, order.name).data['price']
        #price = pos.data['dPrePos'][flagDtm, flagName] / pos.data['uPrePos'][flagDtm, flagName]
        #pdb.set_trace()
        pos.data['dTrade'][flagDtm, flagName] = order.data['order'] * price
        pos.data['dTargetPos'][flagDtm, flagName] = pos.data['dPrePos'][flagDtm, flagName] + pos.data['dTrade'][flagDtm, flagName]
        pos.data['uTargetPos'][flagDtm, flagName] = pos.data['uPrePos'][flagDtm, flagName] + pos.data['uTrade'][flagDtm, flagName]

        pos.data['dCash'][flagDtm, flagName] = -pos.data['dTrade'][flagDtm, flagName]
        pos.data['dTcost'][flagDtm, flagName] = fTcost(arr.array(order.dtm), arr.array(order.name))
        return pos
    return f


def fUniETH(dtm):
    return numpy.array(['ETHUSD'])


def demo():
    '''
    a simulation demo
    trade ETH everyday at 12:00 p.m.
    '''
    dtm = cal.usCal()[datetime.datetime(2016, 1, 1): datetime.datetime(2017, 1, 1)] + numpy.timedelta64(12, 'h')
    gPrice = _priceETH()
    dtm_all = numpy.sort(numpy.append(gPrice.dtm, dtm))
    flag = arr.isin(dtm_all, gPrice.dtm)
    price = numpy.full(dtm_all.shape, numpy.nan)
    price[flag] = gPrice.data['price']
    price = arr.bleed(price)
    #price = numpy.zeros([dtm_all.shape[0], 1])
    g = grid_v2.grid([price[~flag][:, None]], dtm, gPrice.name, ['price'])
    fOpt = _ETHOpt(g.select)
    pos = backTestCore(dtm, fUniETH, _retrievePos, fOpt, _updateOrder(g.select),_fixTcost5Bps())  
    return pos


def fake_price_gbm(dtms, start=1., mean=0, std=1e-4):
    '''
    Generate fake geometric brownian motion
    '''
    l = len(dtms)
    x = numpy.random.randn(l) * std
    x[0] = 0.
    price = numpy.cumprod(start + x)
    def price(dtm, name):
        return price[dtms==dtm]
    return price


def demo_1min():
    '''
    a simulation demo
    trade a virtual asset every minute.
    '''

    # we generate dtm from 2015-01-01 to 2019-01-01
    cal1 = cal.cal()
    dtm_start = datetime.datetime(2015, 1, 1)
    dtm_end = datetime.datetime(2019, 1, 1)
    dtms = cal1[dtm_start: dtm_end]
    fprice = fake_price_gbm(dtms)
    def fOpt(dtm, name):
        return numpy.ones([len(dtm), len(name)])
    def fUniverse(dtm):
        return numpy.array(['Bitcoin'])
    def fRetrievePos(dtm, name, fPrice, grid):
        return grid.project(dtm, name)
    def fUpdateOrder(dtm, name, grid):
        import pdb
        pdb.set_trace()
        return None
    def fTcost_5bps(dtm, name, pos):
        import pdb
        pdb.set_trace()
        return None
    pos = backTestCore(dtms, fUniverse, fprice, fRetrievePos, fOpt, fUpdateOrder, fTcost_5bps)
    return





