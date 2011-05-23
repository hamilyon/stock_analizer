"""
"""

from .base import *

#----------------------------------------------------------------------
@Pattern.wrap(1)
def doji(bars):
    """
    """
    return bars[0].low < bars[0].open and \
           bars[0].high > bars[0].close and \
           bars[0].open == bars[0].close


#----------------------------------------------------------------------
@Pattern.wrap(1)
def white_marubozu(bars):
    """
    """
    return bars[0].open == bars[0].low and \
           bars[0].close == bars[0].high and \
           bars[0].open != bars[0].close


#----------------------------------------------------------------------
@Pattern.wrap(1)
def black_marubozu(bars):
    """
    """
    return bars[0].open == bars[0].high and \
           bars[0].close == bars[0].low and \
           bars[0].open != bars[0].close


#----------------------------------------------------------------------
@Pattern.wrap(1)
def dragonfly(bars):
    """
    """
    return bars[0].open == bars[0].high == bars[0].close and \
           bars[0].low < bars[0].close


#----------------------------------------------------------------------
@Pattern.wrap(1)
def gravestone(bars):
    """
    """
    return bars[0].open == bars[0].low == bars[0].close and \
           bars[0].high > bars[0].close

