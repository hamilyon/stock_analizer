"""
"""

import unittest
from market.pattern.base import *


########################################################################
class PatternTestCase(unittest.TestCase):
    """"""

   
    #----------------------------------------------------------------------
    def test_wrapped(self):
        pattern = Pattern.wrap(1)(lambda arr: arr[0] > 5)
        self.assertTrue(pattern( [6] ))
        self.assertFalse(pattern( [4] ))
        
        pattern = Pattern.wrap(1)(lambda arr: arr[0] < 9)
        self.assertTrue(pattern( [7] ))
        self.assertFalse(pattern( [100] ))
        
        pattern = Pattern.wrap(1)(lambda arr: arr[0] == 7)
        self.assertTrue(pattern( [7] ))
        self.assertFalse(pattern( [4] ))
        
    #----------------------------------------------------------------------
    def test_normal(self):
        """"""
        gt5 = Pattern.wrap(1)(lambda arr: arr[0] > 5)
        le7lt5 = Pattern.wrap(2)(lambda arr: arr[0] <= 7 and arr[1] < 5)
        
        pattern = Pattern([gt5, le7lt5])
        self.assertTrue(pattern( [6, 3] ))
        self.assertTrue(pattern( [7, -1] ))
        self.assertFalse(pattern( [10, 3] ))
        self.assertFalse(pattern( [6, 6] ))
        
        pattern = Pattern([None, gt5, None, le7lt5])
        self.assertTrue(pattern( [-42, 6, 1, 3] ))
        self.assertTrue(pattern( [432, 10, 7, -1] ))
        self.assertFalse(pattern( [112, 1, 7, 0] ))
        self.assertFalse(pattern( [-43, 6, 1, 7] ))
        
    #----------------------------------------------------------------------
    def test_and(self):
        """"""
        gt5 = Pattern.wrap(1)(lambda arr: arr[0] > 5)
        le6 = Pattern.wrap(1)(lambda arr: arr[0] <= 6)
        pattern = gt5 & le6
        self.assertTrue(pattern( [6] ))
        self.assertFalse(pattern( [5] ))
        self.assertFalse(pattern( [7] ))
            
    #----------------------------------------------------------------------
    def test_or(self):
        """"""
        lt5 = Pattern.wrap(1)(lambda arr: arr[0] < 5)
        gt7 = Pattern.wrap(1)(lambda arr: arr[0] > 7)
        pattern = lt5 | gt7
        self.assertTrue(pattern( [4] ))
        self.assertTrue(pattern( [10] ))
        self.assertFalse(pattern( [5] ))
        self.assertFalse(pattern( [6] ))
        self.assertFalse(pattern( [7] ))
    
    #----------------------------------------------------------------------
    def test_invert(self):
        """"""
        pattern = Pattern.wrap(1)(lambda arr: arr[0] < 5)
        self.assertTrue(pattern( [4] ))
        self.assertFalse(pattern( [5] ))
        self.assertFalse(pattern( [6] ))

        pattern = ~pattern
        self.assertFalse(pattern( [4] ))
        self.assertTrue(pattern( [5] ))
        self.assertTrue(pattern( [6] ))

    #----------------------------------------------------------------------
    def test_add(self):
        """"""
        lt5 = Pattern.wrap(1)(lambda arr: arr[0] < 5)
        gt7 = Pattern.wrap(1)(lambda arr: arr[0] > 7)
        pattern = lt5 + gt7
        self.assertRaises(ValueError, pattern, [4])
        self.assertTrue(pattern( [4, 8] ))
        self.assertFalse(pattern( [4, 7] ))
        self.assertFalse(pattern( [5, 8] ))
        self.assertFalse(pattern( [100, -100] ))


    #----------------------------------------------------------------------
    def test_complex(self):
        """"""
        lt5 = Pattern.wrap(1)(lambda arr: arr[0] < 5)
        gt7 = Pattern.wrap(1)(lambda arr: arr[0] > 7)
        gt1 = Pattern.wrap(1)(lambda arr: arr[0] > 1)
        lt10 = Pattern.wrap(1)(lambda arr: arr[0] < 10)
        # Too complex pattern. It's possible, but don't do it :)
        pattern = Pattern([lt5, ~(gt1 & lt10) + (lt5 | gt7)])
        self.assertTrue(pattern( [0, 4] ))
        self.assertTrue(pattern( [-100, 100] ))
        self.assertFalse(pattern( [2, 100] ))
        self.assertFalse(pattern( [0, 6] ))
        

    #----------------------------------------------------------------------
    def test_immutable(self):
        """"""
        lt5 = Pattern.wrap(1)(lambda arr: arr[0] < 5)
        with self.assertRaises(TypeError):
            lt5.occurrences = [] # Try to break
        with self.assertRaises(TypeError):
            lt5.occurrences[0] = None # Try to break
        with self.assertRaises(TypeError):
            setattr(lt5, "newattr", "Bad attr")
        
        
        
if __name__ == "__main__":
    unittest.main()