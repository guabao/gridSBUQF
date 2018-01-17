__doc__ = 'market carlendar, has dependency on pandas_market_calendars'


import pandas
import numpy
import datetime

import pandas_market_calendars

import arr



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


class intraCal():
    def __init__(self, cal, tm):
        raise NotImplementedError('Under Construction!')
        return None
