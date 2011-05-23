"""
Unit test for FinamAgent.
"""

import unittest
from datetime import datetime, date, time
from market.data import *
from coverage.providers import testprovider
from market.providers.finam import FinamProvider


########################################################################
class FinamProviderTestCase(unittest.TestCase):
   """"""
      
   #----------------------------------------------------------------------
   def setUp(self):
      self.provider = FinamProvider()
         
   #----------------------------------------------------------------------
   def test_daily(self):
      GAZP = self.provider['GAZP']   
      day = timedelta(days=1)
      data = tuple(GAZP.daily(date(2010, 11, 1), date(2010, 11, 13)))
      self.assertEqual(data, (
         Bar(GAZP, datetime(2010, 11,  1), day, 169.99, 171.40, 169.40, 169.89, 46087533),
         Bar(GAZP, datetime(2010, 11,  2), day, 169.93, 170.50, 168.95, 170.16, 28573798),
         Bar(GAZP, datetime(2010, 11,  3), day, 170.26, 171.00, 169.56, 170.19, 33887892),
         Bar(GAZP, datetime(2010, 11,  8), day, 174.38, 175.35, 173.60, 174.20, 62888228),
         Bar(GAZP, datetime(2010, 11,  9), day, 174.02, 177.44, 174.02, 176.10, 70927999),
         Bar(GAZP, datetime(2010, 11, 10), day, 175.04, 175.51, 173.10, 174.47, 54807302),
         Bar(GAZP, datetime(2010, 11, 11), day, 175.39, 175.74, 172.36, 172.60, 42875766),
         Bar(GAZP, datetime(2010, 11, 12), day, 170.99, 172.80, 169.90, 171.88, 46123354),
         Bar(GAZP, datetime(2010, 11, 13), day, 171.18, 171.91, 170.62, 171.69, 13316997),
         )
      )

   #----------------------------------------------------------------------
   def test_intraday(self):
      GAZP = self.provider['GAZP']   
      minute = timedelta(minutes=1)
      data = tuple(GAZP.intraday(datetime(2011, 1, 11, 10, 40), datetime(2011, 1, 11, 11, 10)))
      self.assertEqual(data, (
         Bar(GAZP, datetime(2011, 1, 11, 10, 40), minute, 193.29, 193.30, 193.15, 193.15, 131070),
         Bar(GAZP, datetime(2011, 1, 11, 10, 41), minute, 193.15, 193.20, 193.11, 193.16, 54798),
         Bar(GAZP, datetime(2011, 1, 11, 10, 42), minute, 193.17, 193.20, 192.91, 193.00, 189081),
         Bar(GAZP, datetime(2011, 1, 11, 10, 43), minute, 192.94, 193.10, 192.91, 192.95, 784218),
         Bar(GAZP, datetime(2011, 1, 11, 10, 44), minute, 192.95, 193.00, 192.90, 192.97, 40220),
         Bar(GAZP, datetime(2011, 1, 11, 10, 45), minute, 192.97, 193.08, 192.92, 193.00, 134868),
         Bar(GAZP, datetime(2011, 1, 11, 10, 46), minute, 193.00, 193.07, 192.90, 192.96, 107785),
         Bar(GAZP, datetime(2011, 1, 11, 10, 47), minute, 192.96, 193.00, 192.91, 193.00, 155529),
         Bar(GAZP, datetime(2011, 1, 11, 10, 48), minute, 192.99, 193.04, 192.92, 192.92, 52927),
         Bar(GAZP, datetime(2011, 1, 11, 10, 49), minute, 192.97, 193.13, 192.93, 193.12, 170472),
         Bar(GAZP, datetime(2011, 1, 11, 10, 50), minute, 193.12, 193.15, 193.02, 193.02, 108814),
         Bar(GAZP, datetime(2011, 1, 11, 10, 51), minute, 193.08, 193.10, 192.98, 193.03, 60060),
         Bar(GAZP, datetime(2011, 1, 11, 10, 52), minute, 193.03, 193.10, 193.00, 193.00, 72902),
         Bar(GAZP, datetime(2011, 1, 11, 10, 53), minute, 193.00, 193.00, 192.97, 192.99, 40161),
         Bar(GAZP, datetime(2011, 1, 11, 10, 54), minute, 192.99, 192.99, 192.87, 192.98, 133649),
         Bar(GAZP, datetime(2011, 1, 11, 10, 55), minute, 192.99, 193.00, 192.89, 192.90, 47516),
         Bar(GAZP, datetime(2011, 1, 11, 10, 56), minute, 192.90, 192.97, 192.75, 192.79, 241821),
         Bar(GAZP, datetime(2011, 1, 11, 10, 57), minute, 192.76, 192.79, 192.73, 192.76, 43760),
         Bar(GAZP, datetime(2011, 1, 11, 10, 58), minute, 192.75, 192.80, 192.74, 192.75, 116904),
         Bar(GAZP, datetime(2011, 1, 11, 10, 59), minute, 192.74, 192.79, 192.74, 192.79, 16556),
         Bar(GAZP, datetime(2011, 1, 11, 11,  0), minute, 192.78, 192.80, 192.32, 192.40, 425637),
         Bar(GAZP, datetime(2011, 1, 11, 11,  1), minute, 192.48, 192.50, 192.36, 192.49, 46450),
         Bar(GAZP, datetime(2011, 1, 11, 11,  2), minute, 192.41, 192.50, 192.21, 192.30, 251371),
         Bar(GAZP, datetime(2011, 1, 11, 11,  3), minute, 192.30, 192.40, 192.19, 192.40, 262207),
         Bar(GAZP, datetime(2011, 1, 11, 11,  4), minute, 192.36, 192.45, 192.33, 192.45, 183564),
         Bar(GAZP, datetime(2011, 1, 11, 11,  5), minute, 192.41, 192.52, 192.30, 192.33, 300426),
         Bar(GAZP, datetime(2011, 1, 11, 11,  6), minute, 192.43, 192.50, 192.40, 192.50, 59430),
         Bar(GAZP, datetime(2011, 1, 11, 11,  7), minute, 192.50, 192.63, 192.46, 192.53, 304795),
         Bar(GAZP, datetime(2011, 1, 11, 11,  8), minute, 192.54, 192.76, 192.52, 192.60, 151769),
         Bar(GAZP, datetime(2011, 1, 11, 11,  9), minute, 192.65, 192.69, 192.61, 192.65, 24430),
         Bar(GAZP, datetime(2011, 1, 11, 11, 10), minute, 192.65, 192.71, 192.60, 192.60, 108188),
         )
      )

   #----------------------------------------------------------------------
   def test_quotes(self):
      ticker = self.provider['GAZP']


if __name__ == '__main__':
   unittest.main()
  