"""
Common types for providers.
"""

from datetime import *
from inspect import getargspec
from functools import partial


########################################################################
class DataError(Exception):
    """
    Base class for different classes of exceptions raising in providers.
    """
    
    #----------------------------------------------------------------------
    def __init(self, hid):
        self.hid = hid


########################################################################
class DataNotFoundError(DataError):
    """
    Raise it when data not exists for the provider.
    """
    
    #----------------------------------------------------------------------
    def __repr__(self):
        return "Can't find any data for {0}. Try other id.".format(self.hid)

    
########################################################################
class TimeHasNotComeError(DataNotFoundError):
    """
    Raises when user request a future data which has not come.
    """

    #----------------------------------------------------------------------
    def __repr__(self):
        return "Can't find any data for {0} in the future.".format(self.hid)
     
        
########################################################################
class DataFetchingError(DataError):
    """
    Raise it when data was found but can't be loaded.
    """
    
    #----------------------------------------------------------------------
    def __init(self, hid, exc):
        super(DataFetchingError, self).__init__(hid)
        self.base = exc
        
    #----------------------------------------------------------------------
    def __repr__(self):
        return "Can't fetch data for {0}. Raised:\n{1}".format(self.hid, self.base)


########################################################################
class InvalidDataFormatError(DataError):
    """
    Raise it when data not exists for the provider.
    """

    #----------------------------------------------------------------------
    def __init(self, hid, sample):
        super(DataFetchingError, self).__init__(hid)
        self.sample = sample    
    
    #----------------------------------------------------------------------
    def __repr__(self):
        return "Invalid data for {0}: {1}".format(self.hid, self.sample)
        

#######################################################################
class Ticker(object):
    
    #----------------------------------------------------------------------
    def __init__(self, provider, symbol, **data):
        self.provider = provider      
        self.symbol = symbol
        self.data = data

    #----------------------------------------------------------------------
    def __getattr__(self, name):
        attr = getattr(self.provider, name)
        try:
            if getargspec(attr).args[1] == 'ticker':
                attr = partial(attr, self)
        except TypeError, IndexError:
            pass # Not a callable or have not args
        return attr
        
    
########################################################################
class DataProvider(object):
    """
    """

    #----------------------------------------------------------------------
    def __getitem__(self, key):
        """"""
        values = self.find(key)
        if values:
            return values[0]
        else:
            raise KeyError("Not found ticker: " + str(key))
        
    #----------------------------------------------------------------------
    def __contains__(self, key):
        """"""
        return key in self.find(key)

    #----------------------------------------------------------------------
    def find(self, query):
        """
        Method returns only available string keys for identify queried ticker.
        """
        raise NotImplementedError("Method 'find' not implemented.")        
        
    #----------------------------------------------------------------------
    def daily(self, ticker, start=1, end=None):
        """
        Creates a stream of the daily data which can be aggregated.
        Start or end expects date format. If start is integer then
        start date will earlier on the given amount of days of end date.
        Start and End are datateime instances.
        """
        delta = timedelta(days=1)

        if not end:
             # Expects trader get new data in the next morging not immediate right after trading session
            end = datetime.combine(date.today(), time()) # Because providers will return data untill but exclude end
        elif type(end) is date:
            end = datetime.combine(end, time())
        else:
            raise TypeError("Unknown type ({0}) of a end date.".format(type(end)))
        
        if isinstance(start, int):
            start = end - delta * start # Will be a datetime
        elif type(start) is date:
            start = datetime.combine(start, time())
        else:
            raise TypeError("Unknown type ({0}) of a start date.".format(type(start)))

        if start >= end:
            raise ValueError("Start datetime is after or equals end.")

        return self.bars(ticker, start, end, delta)
    
    #----------------------------------------------------------------------
    def intraday(self, ticker, start=1, end=None):
        """\
        Creates a generator which return requested data in minutely bars.
        
        End date is the time to which the data will be requested.
        End can be a date or datetime instance. When it was set as a date,
        end date converts to datetime with time as zero. If end was set as
        None than end will set as today and converts with date conversion rules
        for end date. If end was set as a datetime instance it floors to minutes
        (seconds and microseconds become 0). You also can set end as time. In this
        case end will convert to today's time.
        
        Start date is a time for from data requested. It can be set as None, int,
        date, time or datetime. If it was set as None 0:00 of today will be used.
        If start set as int it means minutes before end. If set as date than 0:00
        of that day will be used. If it set as time it will convert to a 
        corresponding today's time. If you set start as a datetime instance it will
        using directly, but if seconds or microseconds aren't euqal 0 start datetime
        will ceiling to a next minute.
        """
        delta = timedelta(minutes=1)

        if not end:
             # Expects trader get new data in the next morging not immediate right after trading session
            end = datetime.now() # Because providers will return data untill but exclude end
        if type(end) is date:
            end = datetime.combine(end, time()) # Datetime flooring
        elif type(end) is time:
            end = datetime.combine(date.today(), end) # Convert to today's time
        if type(end) is datetime:
            end = end.replace(second=0, microsecond=0) # Datetime flooring
        else:
            raise TypeError("Unknown type ({0}) of a end datetime.".format(type(end)))
        
        if not start:
            start = date.today() # From start of this day
        elif isinstance(start, int):
            start = end - delta * start # Will be a datetime
        if type(start) is date:
            start = datetime.combine(start, time()) # Datetime flooring
        elif type(start) is time:
            start = datetime.combine(date.today(), start) # Converts to today's time
        if type(start) is datetime:
            if start.second or start.microsecond:
                start += delta # Increase for ceiling
            start = start.replace(second=0, microsecond=0) # Datetime ceiling
        else:
            raise TypeError("Unknown type ({0}) of a start datetime.".format(type(start)))

        if start >= end:
            raise ValueError("Start datetime is after or equals end.")
                
        return self.bars(ticker, start, end, delta)
    
        
    