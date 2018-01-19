__doc__ = 'eth sim project'

import os


import numpy

from gridSBUQF import grid_v2, frameBackTest
from gridSBUQF.util import arr, cache

from lib import tib


########
# price data
########

def _rawPriceETH():
    path = os.path.dirname(os.path.abspath(__file__))
    mx = numpy.load(path + '/ETHData.csv.npy')
    #import pdb
    #pdb.set_trace()
    dtm = numpy.array(mx[0], dtype='datetime64[s]')
    price = mx[1]
    name = numpy.array(['ETHUSD'])
    return grid_v2.grid([price[:, None]], dtm, name, ['price'])


def priceETH1min():
    g0 = _rawPriceETH()
    dtm0 = g0.dtm[0]
    dtm1 = g0.dtm[-1]
    dtms = numpy.arange(dtm0, dtm1, numpy.timedelta64(60, 's'))
    g1 = g0.select(dtms, g0.name)
    price = arr.bleed(g1.data['price'].ravel())
    logret = numpy.append(0, numpy.diff(numpy.log(price)))
    g1.addFields([price[:, None], logret[:, None]], fields=['price', 'logret'])
    #g1.addFields(logret[:, None], ['logret'])
    return g1


@cache.cacheMemory
def priceETH1hour():
    g0 = _rawPriceETH()
    dtm0 = g0.dtm[0]
    dtm1 = g0.dtm[-1]
    dtms = numpy.arange(dtm0, dtm1, numpy.timedelta64(3600, 's'))
    g1 = g0.select(dtms, g0.name)
    price = arr.bleed(g1.data['price'].ravel())
    logret = numpy.append(0, numpy.diff(numpy.log(price)))
    g1.addFields([price[:, None], logret[:, None]], fields=['price', 'logret'])
    #g1.addFields(logret[:, None], ['logret'])
    return g1


@cache.cacheMemory
def _predETH():
    pole = tib.cheb_pts(8)
    g = priceETH1hour()
    pred, _, _ = tib.tibrls(pole, g.data['logret'].ravel())
    g.addFields([pred[:-1, None]], fields=['pred'])
    return g


########
# universe
########

def uniETH(dtm): return numpy.array(['ETHUSD'])



########
# retrieve position
########


def retrievePos(dtm, name, fprice, pos):
    dtm = arr.array(dtm)
    name = arr.array(name)
    assert pos.__dtmSorted__ == True
    index = numpy.argwhere(numpy.isin(pos.dtm, dtm))[0]
    uPre = pos.data['uPrePos'][index-1] + pos.data['uTrade'][index-1]
    dPre = uPre * fprice(dtm, name).data['price'].ravel()
    pos.data['uPrePos'][index] = uPre
    pos.data['dPrePos'][index] = dPre
    return pos.select(dtm, name).data['dPrePos']



########
# optimization
########



def fOptETH(fPred):
    def fOpt(dtm, name, fPrice, pre_pos):
        pred = fPred(dtm, name).data['pred']
        price = fPrice(dtm, name).data['price'].ravel()
        return grid_v2.grid([numpy.sign(pred) - pre_pos / price], arr.array(dtm), arr.array(name), ['order'])
    return fOpt


########
# transaction cost
########

def fTcost5Bps(dtm, name):
    return priceETH1hour().select(dtm, name).data['price']



########
# filler
########


def fillerAllFill(pos, order, fPrice, fTcost):
    assert pos.__dtmSorted__
    assert pos.__nameSorted__
    assert len(order.dtm) == 1
    order.sortName()
    dtm = order.dtm
    name = order.name
    flagDtm = numpy.isin(pos.dtm, dtm)
    flagName = numpy.isin(pos.name, name)
    flag = flagDtm[:, None] * flagName[None, :]
    pos.data['uTrade'][flag] = order.data['order'][0]
    pos.data['uTargetPos'][flag] = pos.data['uPrePos'][flag] + pos.data['uTrade'][flag]
    price = fPrice(dtm, pos.name).data['price']
    pos.data['dTrade'][flagDtm] = pos.data['uTrade'][flagDtm] * price
    pos.data['dTargetPos'][flagDtm] = pos.data['uTargetPos'][flagDtm] * price
    pos.data['dCash'][flagDtm] = -pos.data['dTrade'][flagDtm]
    pos.data['dTcost'][flagDtm] = fTcost(dtm, name) * pos.data['dTrade'][flagDtm]
    return pos


########
# test
########


def testSim():
    import pdb
    g = priceETH1hour()
    dtms = g.dtm[1:]
    funi = uniETH
    fprice = g.select
    fretrieve = retrievePos 
    fopt = fOptETH(_predETH().select)
    ffiller = fillerAllFill 
    ftcost = fTcost5Bps
    #pdb.set_trace()
    return frameBackTest.backTestCore(dtms, funi, fprice, fretrieve, fopt, ffiller, ftcost)
