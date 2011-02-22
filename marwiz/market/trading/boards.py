"""
This library has an unique architecture. For calculation of indicators we use boards
which also public values. Values of boards should not be changed from the outside.
It is very convenient concept. It allows to read out values from set of places
for different tasks. For updating board it have to declare methods with or without
arguments. Methods can change values in board using keys for get access to it as to dict.
Look into examples to know how to work with it.
"""

from functools import wraps


########################################################################
class putup(object):
    """
    Decorator. Uses with method of board classes.
    Stores returned values from decorated method to a dictionary class
    owned decorated method.
    """

    #----------------------------------------------------------------------
    def __init__(self, *keys):
        """
        Set keys for storing returned values.
        """
        self.keys = keys
    
    #----------------------------------------------------------------------
    def __call__(self, func):
        """
        Creating a decorator which stores returned values from method.
        """
        if len(self.keys) > 1:
            @wraps(func)
            def wrapper(board, *args, **kwds): # board is self for Board instances
                returned = func(board, *args, **kwds)
                board.update(dict(zip(self.keys, returned)))
            return wrapper
        else:
            @wraps(func)
            def wrapper(board, *args, **kwds): # board is self for Board instances
                board[self.keys[0]] = func(board, *args, **kwds)
            return wrapper
    

########################################################################
class Board(dict): # TODO inherite PrefixedMethods
    """
    Classes to puts up indicator values.
    
    To define your method use prefix 'get'.
    """
    pass


    
        
        
    
    