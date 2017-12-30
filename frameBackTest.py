__doc__ = 'Framework of back test.'




def backTestCore(dtms, fUniverse, fLookPrice, fDividends, fSplits, fRolling, fOptimization):

    #   back test frame work
    #
    #   description of inputs:
    #
    #   dtms        :   1 dimension numpy array indicating the datetime range in the simulation
    #   fUniverse   :   a function returns a 1 dimension numpy array including the trading universe for the input dtm
    #   fLookPrice  :   a function returns a grid including the look price at dtm for the input dtm and name
    #   fDividends  :   a function returns a grid including the dividend data at dtm for the input dtm and name
    #   fSplits     :   a function returns a grid including the splits data at dtm for the input dtm and name
    #   fRolling    :   a function update the position upto current trading cycle given last cycle position and price function
    #   fOptimization:  a function returns the target position given position grid

    #initialization

    name_all = union([fUniverse(dtmi) for dtmi in dtms])    # get all the names
    pos = pos_init(dtms, names)                               # initialize back test position
    
    for i, dtmi in enumerate(dtm):
        
        name_active = fUniverse(dtmi)
        pos = pos if dtmi == dtm[0] else fRolling(dtm[i-1], dtm, pos) # unfinished, need adjust
        
        pre_position = pos.select(dtmi, name_active) # unfinished, need adjust
        target_position = fOptimization(pos)

        pos.write(target_position)


    return pos


def _posInit(dtm, name):
    n = dtm.shape[0]
    m = name.shape[0]
    dPrePos = numpy.zeros((n, m))
    uPrePos = numpy.zeros((n. m))
    dTrade = numpy.zeros((n, m))
    uTrade = numpy.zeros((n, m))
    dTargetPos = numpy.zeros((n, m))
    uTargetPos = numpy.zeros((n, m))
    return None
