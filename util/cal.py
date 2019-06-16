__doc__ = 'market carlendar, has dependency on pandas_market_calendars'
__pyVersion__ = 'python3'

import pandas
import numpy
import datetime

import pandas_market_calendars

from . import arr

_NOW=datetime.datetime.now()
_NOW_DT64=numpy.datetime64(_NOW)
_TODAY=_NOW.date()
_TODAY_DT64=numpy.datetime64(_TODAY)



class usCal():
    def __init__(self, intraSeconds=None):
        self.seconds = intraSeconds
        self.cal = pandas_market_calendars.get_calendar('NYSE')  
        self.timeZone = "UTC-5"
        
        # mark holidays on TAQ
        self.holidays = self.cal.holidays().holidays
        flag = self.holidays > numpy.datetime64("1993-01-01") # TAQ start from 1993
        self.holidays = tuple(numpy.array(self.holidays)[flag])

        return None

    def period(self, day0=datetime.date.today(), day1=datetime.date.today()):
        periods = self.cal.valid_days(start_date = day0, end_date = day1)
        return periods[:-1].values if len(periods) > 1 else periods.values

    def day(self, day0=datetime.date.today(), n=0):
        if isinstance(day0, datetime.datetime) or isinstance(day0, datetime.date):
            day0 = pandas.Timestamp(day0)
        assert isinstance(day0, pandas.Timestamp), 'Invalid day0 type!'
        today = day0
        targetDay = today + pandas.Timedelta(days = n + 5 * numpy.sign(n))
        fExtract = lambda x: (x.year, x.month, x.day)
        if n >= 0:
            validDays = self.period(today, targetDay)
        else:
            validDays = self.period(targetDay, today)
        l = len(validDays)
        if l > numpy.abs(n):
            return validDays[n].values
        else:
            return self.day(targetDay, n - (l - 1) * numpy.sign(n))
            #self.day(n - (l - 1) * numpy.sign(n), targetDay)

    def next(self, day0=datetime.date.today(), n=1):
        return self.day(day0, n)

    def pre(self, day0=datetime.date.today(), n=1):
        return self.day(day0, -n)

    def isHoliday(self, day):
        return arr.isin(numpy.array(day, dtype = 'datetime64[D]'), self.holidays)

    def isTradingDay(self, day):
        return ~self.isHoliday(day)

    def __getslice__(self, i, j):
        return self.period(i, j)

    def __getitem__(self, key):
        assert key.step is None, "Not Implemented."
        return self.__getslice__(key.start, key.stop)
        #return self.period(key.start, key.stop)


class calDay():
    '''
    A general day calendar, would support some trading system like crypto
    '''
    def __init__(self):
        self.timeZone = "UTC-5"
        #raise NotImplementedError('Under Construction!')
        return None

    def day(self, day0=_TODAY_DT64, n=0):
        '''
        Day count function, return day0 +(-) n day
        '''
        return numpy.datetime64(day0) + numpy.timedelta64(n, 'D')

    def next(self, day0=_TODAY_DT64, n=1):
        return self.day(day0, n)

    def prev(self, day0=_TODAY_DT64, n=1):
        return self.day(day0, -n)

    #def __getslice__(self, start, end):
    def __getitem__(self, sliced):
        '''
        Support cal[start:end] function 
        '''
        start = numpy.datetime64(sliced.start)
        stop = numpy.datetime64(sliced.stop)
        if sliced.step:
            if not isinstance(sliced.step, numpy.timedelta64):
                step = numpy.timedelta64(sliced.step)
        else:
            step = numpy.timedelta64(1, 'D')
        assert (start - start.astype('datetime64[D]')).item().total_seconds()==0, 'Start dte should be a date!'
        assert (stop - stop.astype('datetime64[D]')).item().total_seconds()==0, 'Stop dte should be a date!'
        assert step==numpy.timedelta64(1,'D'), 'Only support 1 day step now!'
        return numpy.arange(start, stop, step)

class cal():
    '''
    A general intraday calendar, would support some trading system like crypto
    '''
    def __init__(self, timedelta=numpy.timedelta64(1,'m')):
        self.timedelta = timedelta
        return None

    def __getitem__(self, sliced):
        '''
        Support cal[start:end] function 
        '''
        start = numpy.datetime64(sliced.start)
        stop = numpy.datetime64(sliced.stop)
        assert sliced.step is None, 'Step in slice should be None!'
        return numpy.arange(start, stop, self.timedelta)





