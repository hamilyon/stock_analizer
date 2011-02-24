"""
This module contains BASE classes of indicators ONLY.

I'm using iterating conception for indicators calculating.
Indicators are calculated just as it was done by our ancestors
when there wasn't any computer. It works faster than a window-based
calculation method which is used in the largest part of a trading software.

There are two types of indicators: array-processing and step-poicessing.
It's my own differentiation into two types:

-> Array-Processing indicators are indicators which calculating same as
window-based indicators. You have an array and calculate values on
values containing in the array. The best example is the indicator
which calculates a maximum or a minimum in the array. Other example is
the simple moving average indicator but we have made it more effectively.

-> Step-processing indicators are indicators which calculating continuously
and based on all received data. You have not an data array. You have only
a new value and any data you saved. The best example is the indicator
which calculates an absolute maximum or an absolute minimum in the all
recieved data. Other example is the exponential moving average which is
calculated step by step when new data is recieved.

"""

from __future__ import division


def skipNone(x): return x == None

def skipFalse(x): return not x

def noskip(x): return False


########################################################################
class Indicator(list):
    """
    Base class for indicators. Can explore input and output parameters and
    accumulate they into list.
    """
    
    #----------------------------------------------------------------------
    def __init__(self):
        super(Indicator, self).__init__(self.defaults)
    
    #----------------------------------------------------------------------
    def isvalid(self, input_values):
        """
        Function which automatically checks input values with correspond skippers.
        """
        return not any([x[0](x[1]) for x in zip(self.skippers, input_values)])

    #----------------------------------------------------------------------
    def update(self, *values):
        """
        Methods for receiving new values.
        """
        raise NotImplementedError()


########################################################################
class ArrayProcessor(Indicator):
    """
    Accumulate input values in an array and calculate indicator's value with that values.
    For creating a new inidicator follow next steps:
    1. Inherit this class at first.
    2. Declare input and output parameters.
    3. Create your own calculate method.
    4. Add your actions when value appended or removed.
    """

    #----------------------------------------------------------------------
    def __init__(self, period):
        super(ArrayProcessor, self).__init__()
        self.period = period
        self.limit = self.period
        self.array = []

    #----------------------------------------------------------------------
    def update(self, *values):
        """
        Extended indicator's routine.
        Calling by user for update an indicator's value. This method calls until an array isn't full.
        When array is full this method will changed with work method.
        """
        # Accumulate data.
        if self.isvalid(values):
            self.preappend(*values)
            self.array.append(values)
            # There is enough data. Calculate first result.
            if len(self.array) >= self.limit:
                # Start to calculate.
                self.update = self.work
                # Calculate first value when array of data is full
                self.calculate(*values)

    #----------------------------------------------------------------------
    def work(self, *values):
        """
        Main indicator's routine.
        """
        if self.isvalid(values):
            # Append newest and pop oldest value if it isn't NaN.
            self.preappend(*values)
            self.array.append(values)
            self.postremove(*self.array.pop(0))
            # Return last or new result if data was updated.
            self.calculate(*values)

    #----------------------------------------------------------------------
    def preappend(self, *newest):
        """
        Calling before a new value will appended to the array.
        You can override it.
        """
        pass

    #----------------------------------------------------------------------
    def postremove(self, *oldest): 
        """
        Calling after an oldest value have removed from the array.
        You can override it.
        """
        pass

    #----------------------------------------------------------------------
    def calculate(self, *values):
        """
        Your main calculation routine must to be here.
        Store indicator's values in instance's fields.
        You must to override it.
        """
        raise NotImplementedError()


########################################################################
class StepProcessor(Indicator):
    """
    Process input values step-by-step and update (aggregate) indicator value.
    For creating a new inidicator follow next steps:
    1. Inherit this class at first.
    2. Declare input and output parameters.
    3. Create your own calculate method.
    4. Add your actions when first value added.
    """

    #----------------------------------------------------------------------
    def __init__(self, period):
        super(StepProcessor, self).__init__()
        self.period = period
        self.limit = self.period        
        self.count = 0

    #----------------------------------------------------------------------
    def update(self, *values):
        """
        Extended indicator's routine.
        Calling by user for update an indicator's value. This method calls until method
        have called n times equals period.
        When array is full this method will changed with work method.
        """
        if self.isvalid(values):
            # Calculating from first when it was set in constructor
            if hasattr(self, '_first'):
                self.calculate(*values)
            else:
                self._first = values
                self.firstadded(*self._first)
            self.count += 1
            if self.count == self.limit:
                del self.count
                # Start to calculate.
                self.update = self.work

    #----------------------------------------------------------------------
    def work(self, *values):
        """
        Main indicator's routine.
        """
        if self.isvalid(values):
            # Return last or new result if data was updated.
            self.calculate(*values)

    #----------------------------------------------------------------------
    def firstadded(self, *values):
        """
        Calling when first value was get. If you need to calculate initial values for
        calculate method fo it here.
        """
        pass

    #----------------------------------------------------------------------
    def calculate(self, *values):
        """
        Your main calculation routine must to be here.
        Store indicator's values in instance's fields.
        You must to override it.
        """
        raise NotImplementedError()


########################################################################
class PartialGenerator(object):
    """
    This class is usesd for generating partial initialized indicator classes.
    """

    #----------------------------------------------------------------------
    @classmethod
    def partial(cls, name, doc, **kwargs):
        """
        Generate a new type based on a calling class with some named
        parameters preset. skippers and Outpust parameters got from
        skippers and defaults of a super class.
        """
        attr = {}
        def __init__(self, *prms, **nprms):
            kwargs.update(nprms)
            super(self.__class__, self).__init__(*prms, **kwargs)
        attr['__init__'] = __init__
        attr['__doc__'] = doc
        #attr.update(dict(cls.skippers))  # Bug already fixed in __new__ 
        #attr.update(dict(cls.defaults)) #  of ParameterSequencer metaclass
        return type(name, (cls,), attr)


########################################################################
class FuncProcessor(ArrayProcessor, PartialGenerator):
    """
    Calculates function for each first value of each array cell of the data.
    """

    skippers = (skipNone,)
    defaults = (None,)    
    
    #----------------------------------------------------------------------
    def __init__(self, period, func, reduce=False): # Don't reduce by default
        super(FuncProcessor, self).__init__(period)
        self.func = func
        self.calculate = self.calculateReduce if reduce else self.calculatePlain

    #----------------------------------------------------------------------
    def calculateReduce(self, *values):
        "Calls if self.reduce is True."
        result = self.array[0][0]
        for next in self.array[1:]:
            result = self.func(result, next[0])
        self[0] = result

    #----------------------------------------------------------------------
    def calculatePlain(self, *values):
        "Calls if self.reduce is False."
        self[0] = self.func([value[0] for value in self.array])


########################################################################
class AggregateProcessor(StepProcessor, PartialGenerator):
    """
    Calculates function with the previous result and a new value.
    This function works like 'reduce' based on stream processing.
    """

    skippers = (skipNone,)
    defaults = (None,)    
    
    #----------------------------------------------------------------------
    def __init__(self, func, period=1, plain=False): # Reduce by default
        super(AggregateProcessor, self).__init__(period)
        self.func = func
        if plain:
            # Skip calling of self.firstadded and calls self.calculate instead
            self._first = True
            self.calculate = self.calculatePlain
        else:
            self.calculate = self.calculateReduce

    #----------------------------------------------------------------------
    def firstadded(self, *values):
        self[0] = values[0]

    #----------------------------------------------------------------------
    def calculateReduce(self, *values):
        "Calls if self.plain is False."
        self[0] = self.func(self[0], values[0])

    #----------------------------------------------------------------------
    def calculatePlain(self, *values):
        "Calls if self.plain is True."
        self[0] = self.func(values[0])

    
########################################################################
class Filter(StepProcessor, PartialGenerator):
    """
    Base class for creating stream filters.
    * Stateful is a filtor which keep the lastest value.
    * Stateless every time switched to None when input
    value haven't met the condition.
    """
    
    skippers = (skipNone,)
    defaults = (None,)    

    #----------------------------------------------------------------------
    def __init__(self, comparator, base=None, asbase=False):
        """Constructor"""
        super(Filter, self).__init__(1)
        self._first = True
        self.comparator = comparator
        self.base = base
        self.asbase = asbase
    
    #----------------------------------------------------------------------
    def calculate(self, price):
        """"""
        if not self.asbase and self.comparator(price, self.base) or \
           self.asbase and self.comparator(self.base, price):
            self[0] = price
        else:
            self[0] = self.defaults[0]
               

########################################################################
class Chain(Indicator):
    """
    Get input arguments from first indicator, and defaults from last.
    """

    #----------------------------------------------------------------------
    def __init__(self, *indicators):
        self.indicators = indicators
        # Override skippers and defaults
        self.skippers = self.indicators[0].skippers # Expected one or more indicators
        self.defaults = self.indicators[-1].defaults
        self.parameters = self.skippers + self.defaults

    #----------------------------------------------------------------------
    def update(self, *values):
        """
        Transfer values from one indicator to another.
        """
        for indicator in self.indicators:
            indicator.update(*values)
            values = indicator
        self[:] = self.indicators[-1]

    #----------------------------------------------------------------------
    def __getattr__(self, name):
        """
        Return attributes from the lastest element of a chain.
        """
        return getattr(self.indicators[-1], name)        

    
       