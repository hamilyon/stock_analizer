"""
Test case for Board.
"""

import unittest
from market.trading.boards import *


########################################################################
class TestBoard(Board):
    """
    Board for testing.
    """
    
    #----------------------------------------------------------------------
    @putup("Arg 1", "Arg 2")
    def method_norm(self, value):
        """
        Normal method.
        """
        return value, value

    #----------------------------------------------------------------------
    @putup("Arg 1")
    def method_one(self, value):
        """
        Return one value. Not tuple.
        """
        return value

    #----------------------------------------------------------------------
    @putup("Arg 1", "Arg 2")
    def method_largein(self, value):
        """
        Return less values than declared.
        """
        return (value,)

    #----------------------------------------------------------------------
    @putup("Arg 1", "Arg 2", "Arg 3")
    def method_largeout(self, value):
        """
        Return less values than declared.
        """
        return (value,)

    #----------------------------------------------------------------------
    @putup("Arg 1", "Arg 2")
    def method_nottuple(self, value):
        """
        Normal method.
        """
        return value
    

########################################################################
class BoardsTestCase(unittest.TestCase):
    """
    Test case for testing a functionallity of Boards.
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        self.board = TestBoard()
        
    #----------------------------------------------------------------------
    def test_dict(self):
        """
        Testing access with keys.
        """
        self.assertTrue(hasattr(self.board, "__getitem__"))
        self.assertTrue(hasattr(self.board, "__setitem__"))
        self.board['key'] = "value"
        self.assertEqual(self.board['key'], "value")
        
    #----------------------------------------------------------------------
    def test_putups(self):
        """
        Testing 'putup' decorator.
        """
        self.board.method_norm(1)
        self.assertDictContainsSubset({'Arg 1': 1, 'Arg 2': 1}, self.board)
        self.board.method_one(2)
        self.assertDictContainsSubset({'Arg 1': 2, 'Arg 2': 1}, self.board)
        self.board.method_largein(3)
        self.assertDictContainsSubset({'Arg 1': 3, 'Arg 2': 1}, self.board)
        self.board.method_largeout(4)
        self.assertDictContainsSubset({'Arg 1': 4, 'Arg 2': 1}, self.board) # No 'Arg 3'
        self.assertRaises(TypeError, self.board.method_nottuple, 5)
        
        
if __name__ == '__main__':
    unittest.main()
   