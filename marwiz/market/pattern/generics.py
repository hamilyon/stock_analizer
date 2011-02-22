"""
"""

from .base import *


#----------------------------------------------------------------------
@Pattern.wrap(2)
def gap_up(bars):
    """
    """
    return bars[0].high < bars[1].low


#----------------------------------------------------------------------
@Pattern.wrap(2)
def gap_down(bars):
    """
    """
    return bars[0].low > bars[1].high


#----------------------------------------------------------------------
@Pattern.wrap(1)
def bull(bars):
    """
    Return True when price growed up.
    """
    return bars[0].open < bars[0].close


#----------------------------------------------------------------------
@Pattern.wrap(1)
def bear(bars):
    """
    Return True when price fall down.
    """
    return bars[0].open > bars[0].close


#----------------------------------------------------------------------
@Pattern.wrap(1)
def hold(bars):
    """
    Return True when price haven't canged.
    """
    # High and low can be different
    return bars[0].open == bars[0].close


#----------------------------------------------------------------------
@Pattern.wrap(1)
def flat(bars):
    """
    Return True when high, low, open, close are equals.
    """
     # Open and close arent grather than high and less than low. Skip them.
    return bars[0].high == bars[0].low

