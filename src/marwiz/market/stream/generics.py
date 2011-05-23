"""
This module contains indicators:
     Min     - (Minimum)
     Max     - (Maximum)
     Sum     - (Summ)
     Prod    - (Product)
     AbsMin  - (Absolute Minimum)
     AbsMax  - (Absolute Maximum)
     AbsSum  - (Absolute Summ)
     AbsProd - (Absolute Product)
     Ceil    - (Ceiling)
     Floor   - (Floor)
     Round   - (Round)
     Sign    - (Sign)
     Delay   - (Delay)
     Cross   - (Crossing of "two lines")
     Keeper  - (Keep not NaN value)
"""

from operator import mul, add
from math import ceil, floor, copysign
from functools import partial
from .base import *   


########################################################################
Min = FuncProcessor.partial("Min",
    """
    Calculates Minimum in an array.
    """,
    func=min)


########################################################################
Max = FuncProcessor.partial("Max",
    """
    Calculates Maximum in an array.
    """,
    func=max)


########################################################################
Sum = FuncProcessor.partial("Sum",
    """
    Summ data in an array.
    """,
    func=sum)


########################################################################
Prod = FuncProcessor.partial("Prod",
    """
    Product of data in an array.
    """,
    func=mul, reduce=True)


########################################################################
AbsMin = AggregateProcessor.partial("AbsMin",
    """
    Minimum for all data.
    """,
    func=min)


########################################################################
AbsMax = AggregateProcessor.partial("AbsMax",
    """
    Maximum for all data.
    """,
    func=max)


########################################################################
AbsSum = AggregateProcessor.partial("AbsSum",
    """
    Summ for all data.
    """,
    func=add)


########################################################################
AbsProd = AggregateProcessor.partial("AbsProd",
    """
    Product for all data.
    """,
    func=mul)


########################################################################
Ceil = AggregateProcessor.partial("Ceil", 
    """
    Ceiling the last value.
    """,
    func=ceil, plain=True)


########################################################################
Floor = AggregateProcessor.partial("Floor",
    """
    Floor the last value.
    """,
    func=floor, plain=True)


########################################################################
Round = AggregateProcessor.partial("Round",
    """
    Round the last value.
    """,
    func=round, plain=True)


########################################################################
Sign = AggregateProcessor.partial("Sign",
    """
    Sign of the last value.
    """,
    func=partial(copysign, 1), plain=True)


########################################################################
class Delay(ArrayProcessor):
    """
    Return values with delay.
    Useful for getting delayed or forestalled values.
    """

    skippers = (noskip,)

    #----------------------------------------------------------------------
    def __init__(self, period, default=None):
        self.defaults = (default,)
        super(Delay, self).__init__(period)
        self.limit = period + 1
    
    #----------------------------------------------------------------------
    def calculate(self, *values):
        self[0] = self.array[0][0]
        
        
########################################################################
class Cross(StepProcessor):
    """"""

    skippers = (skipNone, skipNone)
    defaults = (None,)
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(Cross, self).__init__(1)
    
    #----------------------------------------------------------------------
    def firstadded(self, first, second):
        """"""
        self.first, self.second = first, second
        
    #----------------------------------------------------------------------
    def calculate(self, first, second):
        """"""
        if self.first < self.second and first > second:
            self[0] = 1
        elif self.first > self.second and first < second:
            self[0] = -1
        else:
            self[0] = self.defaults[0]
        # Save previous values
        self.first, self.second = first, second
        

########################################################################
class Keeper(StepProcessor):
    """
    Uses when you need to keep not NaN values.
    """

    skippers = (skipNone,)
    defaults = (None,)
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(Keeper, self).__init__(1)
        self._first = True
        
    #----------------------------------------------------------------------
    def calculate(self, price):
        """"""
        self[0] = price
        
        
########################################################################
class Counter(StepProcessor):
    """
    Count not None input values.
    """

    skippers = (skipFalse,)
    defaults = (0,)

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(Counter, self).__init__(1)
        self._first = True
        
    def calculate(self, price):
        """"""
        self[0] += 1 # Increase counter
        
    
    
        
        
    
    