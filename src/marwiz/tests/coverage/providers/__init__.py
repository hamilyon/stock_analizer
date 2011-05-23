"""
Unit tests for the Processor based indicators.
"""

import unittest
from market.data import *
from market.providers.base import DataNotFoundError


########################################################################
class DataProviderTestCase(unittest.TestCase):
    """
    Tests providers which returns quotes.
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        """
        Build provider's instance with preset parameters.
        """
        self.provider = self.providerclass(**self.parameters)
        
    #----------------------------------------------------------------------
    @staticmethod
    def maketester(part):
        """
        Walk through all methods, calls they to get data and compare
        with constants.
        """
        def test_method(self):
            fetcher = getattr(self.provider, part['method'])
            arguments = part['arguments']
            dataiter = fetcher(**arguments)
            self.assertEqual(tuple(dataiter), part['data'])
            # Try to get data with not exist ticker
            if 'ticker' in arguments:
                arguments['ticker'] = Market("-").Section("-").Ticker("-")
                self.assertRaises(DataNotFoundError, fetcher, **arguments)
        return test_method
        

        
def testprovider(module, testname, providerclass, data, **parameters):
    """
    Creates unit test class based on AgentTestCase.
    For checking result use data argument and set it to a tuple of dicts
    with the following structure:
    (
        {'method': "method_name",    # Method which will call to get iterable data
         # Set dictionary with named arguments for calling that method.
         'arguments': {'hid': ..., 'start': ..., 'end': ..., other args...},
         'data': ( # Tuple of data units to comparing with values returned with iterator.
             # For instance
             Bar(hid, start, end, ...), # And more
         )
        },
        ... next dictionaries for other methods
    )
    """
    #testname = agentclass.__name__ + "_test"
    locs = dict(providerclass=providerclass,
                data=data,
                parameters=parameters)
    for part in data:
        tester = "test_" + part['method']
        locs[tester] = DataProviderTestCase.maketester(part)
    new = type(testname, (DataProviderTestCase,), locs)
    new.__module__ = module
    return new

               