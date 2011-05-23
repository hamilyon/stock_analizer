"""
"""

import unittest
from datetime import date, time, datetime, timedelta
from time import sleep
from market.providers.base import DataProvider


########################################################################
class TestingProvider(DataProvider):
    
    #----------------------------------------------------------------------
    def bars(self, hid, start, end, period):
        return {'hid': hid,
                'start': start,
                'end': end,
                'period': period}
    
    
########################################################################
class DataProviderTestCase(unittest.TestCase):
    """
    Tests providers which returns quotes.
    """

    #----------------------------------------------------------------------
    def synctime(self):
        """Don't run test if it isn't enough time in the current minute"""
        rest = 60 - datetime.now().second
        if rest < 10:
            sleep(rest) # Wait for the next minute        
    
    #----------------------------------------------------------------------
    def setUp(self):
        self.provider = TestingProvider()
    
    #----------------------------------------------------------------------
    def test_daily_normal(self):
        result = self.provider.daily(None,
                                     date(2010, 1, 1),
                                     date(2010, 12, 31))
        self.assertEqual(result['start'], datetime(2010, 1, 1))
        self.assertEqual(result['end'], datetime(2010, 12, 31))
            
    #----------------------------------------------------------------------
    def test_daily_default(self):
        "Expects the end date is today and the start is yesterday by default."
        result = self.provider.daily(None)
        end = datetime.combine(date.today(), time())
        start = end - timedelta(days=1)
        self.assertEqual(result['start'], start)
        self.assertEqual(result['end'], end)
        
    #----------------------------------------------------------------------
    def test_daily_start_as_int(self):
        "Expects the end date is today and the start is yesterday by default."
        result = self.provider.daily(None, 5, date(2010, 1, 6))
        self.assertEqual(result['start'], datetime(2010, 1, 1))
        self.assertEqual(result['end'], datetime(2010, 1, 6))

    #----------------------------------------------------------------------
    def test_daily_end_as_none(self):
        "Expects the end date is today by default."
        result = self.provider.daily(None, date(2010, 1, 1))
        self.assertEqual(result['start'], datetime(2010, 1, 1))
        self.assertEqual(result['end'], datetime.combine(date.today(), time()))

    #----------------------------------------------------------------------
    def test_daily_swap_inadvertence(self):
        "Expects exception when start is after end."
        with self.assertRaises(ValueError):
            self.provider.daily(None,
                                date(2010, 12, 31),
                                date(2010, 1, 1))

    #----------------------------------------------------------------------
    def test_daily_equal_inadvertence(self):
        "Expects exception when start is equal end. No data in that interval."
        with self.assertRaises(ValueError):
            self.provider.daily(None,
                                date(2010, 1, 1),
                                date(2010, 1, 1))
            
    #----------------------------------------------------------------------
    def test_daily_invalid_start(self):
        "Expects exception when start has invalid type."
        with self.assertRaises(TypeError):
            self.provider.daily(None,
                                datetime(2010, 1, 1),
                                date(2010, 12, 31))

    #----------------------------------------------------------------------
    def test_daily_invalid_end(self):
        "Expects exception when start has invalid type."
        with self.assertRaises(TypeError):
            self.provider.daily(None,
                                date(2010, 1, 1),
                                datetime(2010, 12, 31))
            
    #----------------------------------------------------------------------
    def test_daily_pass_hid(self):
        result = self.provider.daily("AnyKindOfHid")
        self.assertEqual(result['hid'], "AnyKindOfHid")

    #----------------------------------------------------------------------
    def test_daily_check_period(self):
        result = self.provider.daily(None)
        self.assertEqual(result['period'], timedelta(days=1))
             
    #----------------------------------------------------------------------
    def test_intraday_normal(self):
        result = self.provider.intraday(None,
                                     datetime(2010, 1, 1, 12, 0),
                                     datetime(2010, 1, 1, 13, 0))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 12, 0))
        self.assertEqual(result['end'], datetime(2010, 1, 1, 13, 0))
    
    #----------------------------------------------------------------------
    def test_intraday_default(self):
        "Expects the end datetime is now and start is a minute ago."
        self.synctime()
        result = self.provider.intraday(None)
        end = datetime.now().replace(second=0, microsecond=0)
        start = end - timedelta(minutes=1)
        self.assertEqual(result['start'], start)
        self.assertEqual(result['end'], end)
    
    #----------------------------------------------------------------------
    def test_intraday_start_as_none(self):
        "Expects the end datetime is now and start is 0:00 of today."
        self.synctime()
        result = self.provider.intraday(None, start=None)
        start = datetime.combine(date.today(), time())
        end = datetime.now().replace(second=0, microsecond=0)
        self.assertEqual(result['start'], start)
        self.assertEqual(result['end'], end)
    
    #----------------------------------------------------------------------
    def test_intraday_start_as_int(self):
        result = self.provider.intraday(None, 5, datetime(2010, 1, 1, 12, 5))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 12, 0))
        self.assertEqual(result['end'], datetime(2010, 1, 1, 12, 5))
    
    #----------------------------------------------------------------------
    def test_intraday_start_as_date(self):
        result = self.provider.intraday(None,
                                        date(2010, 1, 1),
                                        datetime(2010, 1, 2, 13, 0))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 0, 0))
        self.assertEqual(result['end'], datetime(2010, 1, 2, 13, 0))
    
    #----------------------------------------------------------------------
    def test_intraday_start_as_time(self):
        end = datetime.combine(date.today(), time(15, 59))
        result = self.provider.intraday(None, time(15, 44), end)
        start = datetime.combine(date.today(), time(15, 44))
        self.assertEqual(result['start'], start)
        self.assertEqual(result['end'], end)
    
    #----------------------------------------------------------------------
    def test_intraday_end_as_date(self):
        result = self.provider.intraday(None,
                                        datetime(2010, 1, 1, 14, 41),
                                        date(2010, 1, 2))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 14, 41))
        self.assertEqual(result['end'], datetime(2010, 1, 2, 0, 0))
    
    #----------------------------------------------------------------------
    def test_intraday_end_as_time(self):
        result = self.provider.intraday(None,
                                        datetime(2010, 1, 1, 14, 43),
                                        time(10, 12))
        end = datetime.combine(date.today(), time(10, 12))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 14, 43))
        self.assertEqual(result['end'], end)
    
    #----------------------------------------------------------------------
    def test_intraday_start_ceiling(self):
        # When seconds not 0
        result = self.provider.intraday(None,
                                     datetime(2010, 1, 1, 12, 0, 24),
                                     datetime(2010, 1, 1, 13, 0))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 12, 1))
        self.assertEqual(result['end'], datetime(2010, 1, 1, 13, 0))
        # When microseconds not 0
        result = self.provider.intraday(None,
                                     datetime(2010, 1, 1, 12, 0, 0, 24),
                                     datetime(2010, 1, 1, 13, 0))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 12, 1))
        self.assertEqual(result['end'], datetime(2010, 1, 1, 13, 0))
    
    #----------------------------------------------------------------------
    def test_intraday_end_flooring(self):
        # When seconds not 0
        result = self.provider.intraday(None,
                                     datetime(2010, 1, 1, 12, 0),
                                     datetime(2010, 1, 1, 13, 1, 24))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 12, 0))
        self.assertEqual(result['end'], datetime(2010, 1, 1, 13, 1))
        # When microseconds not 0
        result = self.provider.intraday(None,
                                     datetime(2010, 1, 1, 12, 0),
                                     datetime(2010, 1, 1, 13, 6, 0, 24))
        self.assertEqual(result['start'], datetime(2010, 1, 1, 12, 0))
        self.assertEqual(result['end'], datetime(2010, 1, 1, 13, 6))
    
    #----------------------------------------------------------------------
    def test_intraday_swap_inadvertence(self):
        "Expects exception when start is after end."
        with self.assertRaises(ValueError):
            self.provider.intraday(None,
                                   datetime(2010, 12, 31, 15, 35),
                                   datetime(2010, 1, 1, 9, 43))

    #----------------------------------------------------------------------
    def test_intraday_equal_inadvertence(self):
        "Expects exception when start is equal end. No data in that interval."
        with self.assertRaises(ValueError):
            self.provider.intraday(None,
                                   datetime(2010, 1, 1, 14, 44, 15),
                                   datetime(2010, 1, 1, 14, 15, 43))
    
    #----------------------------------------------------------------------
    def test_intraday_invalid_start(self):
        "Expects exception when start has invalid type."
        with self.assertRaises(TypeError):
            self.provider.daily(None,
                                1423.43,
                                datetime(2010, 12, 31, 12, 32))

    #----------------------------------------------------------------------
    def test_intraday_invalid_end(self):
        "Expects exception when start has invalid type."
        with self.assertRaises(TypeError):
            self.provider.daily(None,
                                date(2010, 1, 1, 10, 32),
                                432.5342)
                
    #----------------------------------------------------------------------
    def test_intraday_pass_hid(self):
        result = self.provider.intraday("AnyKindOfHid")
        self.assertEqual(result['hid'], "AnyKindOfHid")

    #----------------------------------------------------------------------
    def test_intraday_check_period(self):
        result = self.provider.intraday(None)
        self.assertEqual(result['period'], timedelta(minutes=1))

    
if __name__ == '__main__':
    unittest.main()
  