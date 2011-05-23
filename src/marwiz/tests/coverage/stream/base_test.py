"""
Unit tests for indicators from marketwizard.indicators.averages module.
"""

import unittest
from coverage.stream import testindicator
from market.stream.base import Chain
from market.stream.averages import EMA
from market.stream.generics import Max


#----------------------------------------------------------------------
Chain_Test = testindicator(__name__, "Chain_Test",
#----------------------------------------------------------------------
Chain, (
    ((58.90,), (None,)),
    ((51.53,), (58.90,)),
    ((50.23,), (55.95,)),
    ((56.43,), (54.77,)),
    ((64.48,), (58.65,)),
    ((51.82,), (58.65,)),
    ((36.13,), (55.92,)),
    ((47.64,), (48.00,)),
    ((57.88,), (51.87,)),
    ((52.50,), (52.12,)),
    ((53.62,), (52.72,)),
    ((61.95,), (56.41,)),
    ((77.86,), (64.99,)),
    ((71.11,), (67.44,)),
    ((81.03,), (72.88,)),
    ((95.18,), (81.80,)),
    ((96.38,), (87.63,)),
    ((121.58,), (101.21,)),
    ((138.58,), (116.16,)),
), EMA(4), Max(2))


# TODO: Check tests coverage

if __name__ == '__main__':
    unittest.main()
