"""
This module contains indicators:
     EMA     - (Exponential Moving Average)
     OWMA    - (Ordered Weighted Moving Average)
     SMA     - (Simple Moving Average)
     WMA     - (Weighted Moving Average)
"""

from __future__ import division
from .base import *

    
########################################################################
class EMA(StepProcessor):
    """
    Calculates Exponential Moving Average.
    """

    skippers = (skipNone,)
    defaults = (None,)
    
    #----------------------------------------------------------------------
    def __init__(self, period):
        super(EMA, self).__init__(period)
        self.k = 2 / (period + 1)
        
    #----------------------------------------------------------------------
    def firstadded(self, in_0):
        self[0] = in_0
        
    #----------------------------------------------------------------------
    def calculate(self, in_0):
        self[0] = (in_0 - self[0]) * self.k + self[0]
    

########################################################################
class OWMA(ArrayProcessor):
    """
    Calculates Ordered Weighted Moving Average.
    """

    skippers = (skipNone,)
    defaults = (None,)
    
    #----------------------------------------------------------------------
    def __init__(self, period):
        super(OWMA, self).__init__(period)
        self.weight = 0.5 * period * (period + 1)
        
    #----------------------------------------------------------------------
    def calculate(self, price):
        msum = 0
        for num, value in enumerate(self.array):
            msum += value[0] * (num + 1)
        self[0] = msum / self.weight


########################################################################
class SMA(ArrayProcessor):
    """
    Calculates Simple Moving Average. Look how it's work. It's simple!
    """

    skippers = (skipNone,)
    defaults = (None,)

    #----------------------------------------------------------------------
    def __init__(self, period):
        super(SMA, self).__init__(period)
        self.sum = 0
        
    #----------------------------------------------------------------------
    def preappend(self, pricenew):
        self.sum += pricenew
        
    #----------------------------------------------------------------------
    def postremove(self, priceold):
        self.sum -= priceold
        
    #----------------------------------------------------------------------
    def calculate(self, price):
        self[0] = self.sum / self.period

        
########################################################################
class WMA(ArrayProcessor):
    """
    Calculates Weighted Moving Average.
    """

    skippers = (skipNone,)
    defaults = (None,)

    #----------------------------------------------------------------------
    def __init__(self, period):
        super(WMA, self).__init__(period)
        self.msum = 0
        self.wsum = 0
        
    #----------------------------------------------------------------------
    def preappend(self, price, volume):
        self.msum += price * volume
        self.wsum += volume
        
    #----------------------------------------------------------------------
    def postremove(self, price, volume):
        self.msum -= price * volume
        self.wsum -= volume
        
    #----------------------------------------------------------------------
    def calculate(self, price, volume):
        self[0] = self.msum / self.wsum
       
