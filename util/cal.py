__doc__ = 'market carlendar, has dependency on pandas_market_calendars'


import pandas
import numpy
import datetime
import pandas_market_calendars



class usCal():
    def __init__(self, intraSeconds=None):
        self.seconds = intraSeconds
        self.cal = pandas_market_calendars.get_calendar('NYSE')  
        self.timeZone = "UTC-5"
        return None

    def day(self, n = 0, day0 = datetime.date.today()):
        if isinstance(day0, datetime.datetime) or isinstance(day0, datetime.date):
            day0 = pandas.Timestamp(day0)
        assert isinstance(day0, pandas.Timestamp), 'Invalid day0 type!'
        today = day0
        targetDay = today + pandas.Timedelta(days = n + 5)
        fExtract = lambda x: (x.year, x.month, x.day)
        validDays = self.cal.valid_days(start_date = '%s-%s-%s'%fExtract(today), end_date = '%s-%s-%s'%fExtract(targetDay))
        l = len(validDays)
        if l - 1 >= n:
            return validDays[n]
        else:
            self.day(n - l + 1, targetDay)
