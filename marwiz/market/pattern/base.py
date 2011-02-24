"""
This module contains different 
"""

from collections import Callable
from ..stream import FuncProcessor


########################################################################
class Pattern(object):
    """"""
    
    #----------------------------------------------------------------------
    @staticmethod
    def wrap(quantity):
        """"""
        occurrences = [None] * quantity
        def decorator(func):
            if isinstance(func, Callable):
                func.depth = quantity
                occurrences[-1] = func
                pattern = Pattern(occurrences)
                #pattern.__doc__ = func.__doc__
                return pattern
            else:
                raise ValueError("You can wrap callable objects only.")
        return decorator
   
    #----------------------------------------------------------------------
    def __init__(self, occurrences):
        """Constructor"""
        # Check depths
        for i, r in enumerate(occurrences):
            if r is None:
                continue
            # Set limit of arg in occurrence for this position            
            excess = r.depth - i - 1
            if excess > 0:
                raise ValueError("occurrence in position {0} has too many input values."
                                 " Move it forward on {1} element(s).".format(i, excess))
        super(Pattern, self).__setattr__('occurrences', tuple(occurrences))

    #----------------------------------------------------------------------
    @property
    def depth(self):
        """"""
        return len(self.occurrences)
        
    #----------------------------------------------------------------------
    def __setattr__(self, *args):
        raise TypeError("Can't modify pattern")
    __delattr__ = __setattr__        
        
    #----------------------------------------------------------------------
    def __call__(self, data):
        """"""
        if len(data) != self.depth:
            raise ValueError("Expects {0} elements in data only."
                             .format(self.depth))
        for i, r in enumerate(self.occurrences):
            if r == None:
                continue
            _to = i + 1
            _from = _to - r.depth
            if not r(data[_from:_to]):
                return False
        return True
    
    #----------------------------------------------------------------------
    def __and__(self, other):
        """"""
        return Pattern.wrap(max(self.depth, other.depth)) \
                           (lambda va: self(va[-self.depth:]) and other(va[-other.depth:]))

    #----------------------------------------------------------------------
    def __or__(self, other):
        """"""
        return Pattern.wrap(max(self.depth, other.depth)) \
                           (lambda va: self(va[-self.depth:]) or other(va[-other.depth:]))

    #----------------------------------------------------------------------
    def __invert__(self):
        """"""
        return Pattern.wrap(self.depth)(lambda va: not self(va[-self.depth:]))
        
    #----------------------------------------------------------------------
    def __add__(self, other):
        """"""
        return Pattern(self.occurrences + other.occurrences)
        

########################################################################
class Recognizer(FuncProcessor):
    """"""
    
    # Override parameter
    defaults = (False,)
    
    #----------------------------------------------------------------------
    def __init__(self, pattern):
        """Constructor"""
        super(Recognizer, self).__init__(pattern.depth, pattern)
        
        
        
