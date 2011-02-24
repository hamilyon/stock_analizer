"""
Data types for representing quotes.
"""

from datetime import datetime, date, time, timedelta


#######################################################################
class Bar(object):
    """
    Represents classical bar with open, high, low and close prices
    during fixed interval inclusive data from stamp to till.
    For creating a provider which load bars define in you agent:
        def bars(self, hid, start, end, period)
    start and end have to be datetime instances
    """

    # TODO Add __slots__
    
    #----------------------------------------------------------------------
    def __init__(self,
                 ticker,
                 timestamp,
                 period,
                 open=None,
                 high=None,
                 low=None,
                 close=None,
                 volume=None,
                 interest=None,
                 *args, **kwargs):
        """Constructor"""
        self.ticker = ticker
        self.timestamp = timestamp
        self.period = period
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.interest = interest
            
    #----------------------------------------------------------------------
    def replace(self,
                open=None,
                high=None,
                low=None,
                close=None,
                volume=None,
                interest=None):
        """
        Replace any numeric value in bar.
        """
        return Bar(self.ticker, self.timestamp, self.period,
                   open or self.open,
                   high or self.high,
                   low or self.low,
                   close or self.close,
                   volume or self.volume,
                   interest or self.interest,
                   )
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """Checks equals of all fields even if they are equals None."""
        if not isinstance(other, Bar):
            return False
        if self.ticker != other.ticker:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.period != other.period:
            return False
        if self.open != other.open:
            return False
        if self.high != other.high:
            return False
        if self.low != other.low:
            return False
        if self.close != other.close:
            return False
        if self.volume != other.volume:
            return False
        if self.interest != other.interest:
            return False
        return True
        
    #----------------------------------------------------------------------
    def __ne__(self, other):
        return not self.__eq__(other)
    
    #----------------------------------------------------------------------
    def __repr__(self):
        return "{ticker.symbol}:{timestamp}:{period}:{open};{high};{low};{close};{volume};{interest}".format(**self.__dict__)    
    
    #----------------------------------------------------------------------
    def __add__(self, other):
        """"""
        raise NotImplementedError() # TODO Implement it.
        

#######################################################################   
class Deal(object):
    """
    Implementation of a tick.
        def deals(self, hid, start, end)
    """

    # TODO Add __slots__
    
    #----------------------------------------------------------------------
    def __init__(self,
                 ticker,
                 timestamp,
                 price,
                 volume):
        raise NotImplementedError()
    
    #----------------------------------------------------------------------
    def __add__(self, other):
        """"""
        # Returns bar
        raise NotImplementedError() # TODO Implement it.
    
