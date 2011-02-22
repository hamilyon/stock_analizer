"""
Unit test for FinamAgent.
"""

import unittest
from datetime import datetime, date, time
from market.data import *
from coverage.providers import testprovider
from market.providers.yahoo import YahooProvider


########################################################################
class YahooProviderTestCase(unittest.TestCase):
   """"""
      
   #----------------------------------------------------------------------
   def setUp(self):
      self.provider = YahooProvider()
         
   #----------------------------------------------------------------------
   def test_daily(self):
      YHOO = self.provider['YHOO']   
      day = timedelta(days=1)
      data = tuple(YHOO.daily(date(2010, 3, 16), date(2010, 4, 2)))
      self.assertEqual(data, (
            Bar(YHOO, datetime(2010, 3, 16), day, 16.47, 16.59, 16.23, 16.36, 18309900),
            Bar(YHOO, datetime(2010, 3, 17), day, 16.28, 16.63, 16.28, 16.50, 13754600),
            Bar(YHOO, datetime(2010, 3, 18), day, 16.46, 16.57, 16.32, 16.56, 12626200),
            Bar(YHOO, datetime(2010, 3, 19), day, 16.62, 16.81, 16.34, 16.44, 17871000),
            Bar(YHOO, datetime(2010, 3, 22), day, 16.37, 16.54, 16.32, 16.34, 18743500),
            Bar(YHOO, datetime(2010, 3, 23), day, 16.34, 16.34, 15.97, 16.03, 31875700),
            Bar(YHOO, datetime(2010, 3, 24), day, 16.10, 16.20, 15.92, 16.09, 32654500),
            Bar(YHOO, datetime(2010, 3, 25), day, 16.17, 16.59, 16.14, 16.32, 27487400),
            Bar(YHOO, datetime(2010, 3, 26), day, 16.34, 16.57, 16.31, 16.54, 23224900),
            Bar(YHOO, datetime(2010, 3, 29), day, 16.48, 16.68, 16.47, 16.56, 14902800),
            Bar(YHOO, datetime(2010, 3, 30), day, 16.55, 16.69, 16.39, 16.61, 16204100),
            Bar(YHOO, datetime(2010, 3, 31), day, 16.45, 16.58, 16.42, 16.53, 11996900),
            Bar(YHOO, datetime(2010, 4,  1), day, 16.58, 16.60, 16.22, 16.29, 20103800),
         )
      )

   #----------------------------------------------------------------------
   def test_quotes(self):
      ticker = self.provider['YHOO']
      q = ticker.quotes()
      self.assertEqual(q.name, 'Yahoo! Inc.') 


if __name__ == '__main__':
   unittest.main()
  