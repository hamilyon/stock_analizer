"""
Unit tests for the Processor based indicators.
"""

import unittest
from collections import Sequence
from datetime import datetime, timedelta
from market.data import Bar
from market.providers.base import Ticker


# TODO Add random provider based on distributions

_ticker = Ticker(None, "") # Empty ticker

def _stamp():
   now = datetime(2010, 10, 9)
   delta = timedelta(minutes=1)
   while True:
      till = now + delta
      yield now, till
      now = till

_stamp = _stamp() # Convert to a generator
      
def tBar(o, h, l, c, v, i=None):
   """
   Function to generate sequence of bars for tests.
   """
   s, t = next(_stamp) # stamp, till
   return Bar(_ticker, s, t, o, h, l , c, v, i)


########################################################################
class ProcessorTestCase(unittest.TestCase):
   """
   This class tests indicators. You must to set maxdifference
   and data fields. First contains a max difference
   beetween calculated and constant values in percents.
   It's necessary because float point calculations isn't accurate.
   Second is tuple of tuple pairs which contains input and output constants.
   """

   args_msg = "Incorrect quantity of {what} in {testname} element {line}: {content}"
   tupl_msg = "{what} data isn't in a tuple in {testname} element {line}: {content}"
   
   #----------------------------------------------------------------------
   def setUp(self):
      """
      Build indicator's instance with preset parameters.
      """
      self.indicator = self.indclass(*self.args, **self.parameters)
      
   #----------------------------------------------------------------------
   def test_indicator(self):
      """
      Routine for update indicator with inputs in data constants.
      Compare the result with outputs and check limit of a difference.
      """
      testname = self.__class__.__name__
      indiname = self.indicator.__class__.__name__
      for num, (inputs, outputs) in enumerate(self.data):
         line = num + 1
         
         # Check user set sample data in tuples
         self.assertIsInstance(inputs, tuple, self.tupl_msg.format(what="Input", 
                                                                   testname=testname, 
                                                                   line=line, 
                                                                   content=inputs))
         
         self.assertIsInstance(outputs, tuple, self.tupl_msg.format(what="Output",
                                                                    testname=testname, 
                                                                    line=line, 
                                                                    content=outputs))
         # Try to update indicator with next portion of a data
         try:
            self.indicator.update(*inputs)
         except TypeError:
            self.fail(self.args_msg.format(what="inputs", 
                                           testname=testname, 
                                           line=line, 
                                           content=inputs))
            
         # Get indicator's state (result)
         values = self.indicator
         # Check indicator returns values in a tuple
         self.assertTrue(isinstance(values, Sequence), "Indicator {0} not a sequence."
                               .format(indiname))
         
         # Indicator returns another quantity of data than user set
         self.assertEquals(len(values), len(outputs), msg=self.args_msg.format(what="outputs",
                                                                               testname=testname,
                                                                               line=line,
                                                                               content=outputs))
         # Compare all values on equality
         for i, val in enumerate(values):
            outval = outputs[i]
            if not val == outval: # Pass is two objects absolutelly equal
               # If the difference is grather than limit test fails.
               self.assertAlmostEqual(val, outval, delta=outval*0.001,
                                      msg="Values in {testname} element {line} with {outputs}"
                                          " not equals indicator {indicator} values: {values}"
                                           .format(testname=testname,
                                                   line=line,
                                                   inputs=inputs,
                                                   outputs=outputs,
                                                   indicator=indiname,
                                                   values=values))
               
      
def testindicator(module, testname, indclass, data, *args, **parameters):
    """
    Function for generating new unit test for an indicator.
    You can test any indicator inherited from Processor class.
    Set class of an indicator as the first parameter.
    Send checking data to the second argument as tuple of pairs:
    (
        ((inputs_1), (outputs_1)),
        ((inputs_2), (outputs_2)),
        ...
        ((inputs_n), (outputs_n)),
    )
    For every pair it calls update method of indicator's instance
    initialized with parameters and result of updating compare
    with corresponding outputs. Outputs gets with values method of
    the indicator. If data constant and taken outputs
    aren't equals will fail.
    Returns new type subclassed TestCase.
    """
    #testname = indclass.__name__ + "_test" # Conveniently but not flexibly (
    locs = dict(indclass=indclass,
                data=data,
                args=args,
                parameters=parameters)
    new = type(testname, (ProcessorTestCase,), locs)
    new.__module__ = module
    return new

