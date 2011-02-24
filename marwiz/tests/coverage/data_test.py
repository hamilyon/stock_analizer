"""
Unit tests for the classes from marketwizard.data.quotes module.
"""

import unittest
from datetime import datetime, timedelta
from market.providers.base import Ticker
from market.data import *


########################################################################
class BarTestCase(unittest.TestCase):
    """
    Tests different using parties of the Bar class.
    """

    #----------------------------------------------------------------------
    def setUp(self):
        TICKER = Ticker(None, "")
        START = datetime(2010, 9, 1, 11) # 11:00 of 1st September 2010
        PERIOD = timedelta(hours=1)
        self.sample = Bar(TICKER, START, PERIOD, 110, 130, 100, 120, 1000)
            
    #----------------------------------------------------------------------
    def test_creating(self):
        """
        Tests bar creating, replacing values and direct access to attributes.
        """
        normbar = self.sample
        self.assertIsNotNone(normbar)
        replbar = normbar.replace(open=normbar.close, close=normbar.open)
        self.assertEquals((normbar.ticker,
                           normbar.timestamp,
                           normbar.period,
                           normbar.open,
                           normbar.high,
                           normbar.low,
                           normbar.close,
                           normbar.volume,
                           normbar.interest),
                          (replbar.ticker,
                           replbar.timestamp,
                           replbar.period,
                           replbar.close, # Close and open swaped
                           replbar.high,
                           replbar.low,
                           replbar.open,
                           replbar.volume,
                           replbar.interest))

    #----------------------------------------------------------------------
    def test_equals(self):
        """
        Check equals or not equals methods.
        """
        bar1 = self.sample.replace(open=self.sample.open)
        bar2 = self.sample.replace(close=self.sample.close)
        barx = self.sample.replace(open=self.sample.close)
        self.assertEqual(bar1, bar2)
        self.assertNotEqual(bar1, barx)
        self.assertNotEqual(bar2, barx)
        # Not equal other types!
        self.assertNotEqual(bar1, None)
        self.assertNotEqual(bar2, "")
        self.assertNotEqual(bar1, [1, 2, 3])
        self.assertNotEqual(bar2, {})
        
    
        
if __name__ == '__main__':
    unittest.main()
        