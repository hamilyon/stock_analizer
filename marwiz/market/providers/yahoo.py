"""
"""

import urllib
from collections import namedtuple
from datetime import datetime, timedelta
from xml.etree.ElementTree import ElementTree
from ..data import Bar
from .utils import decapitalize, guess
from .base import DataProvider, Ticker, InvalidDataFormatError


__all__ = ['YahooProvider']


########################################################################
class YahooQuotes(object):
    
    def __init__(self, source):
        self.source = source

    def __dir__(self):
        return self.source.keys()
        
    def __getattr__(self, name):
        if name in self.source:
            val = self.source[name]
            if type(val) is str:
                val = guess(val)
            if not type(val) is str:
                # Keep converted
                self.source[name] = val
            return val
        else:
            return super(YahooQuotes, self).__getattr__(name)
                    

########################################################################
class YahooProvider(DataProvider):
    """
    Provider for data from Yahoo! working with Yahoo! Query Language.
    """

    #----------------------------------------------------------------------
    @staticmethod
    def _yql(table, where=None, reverse=False):
        query = 'select * from ' + table
        wquery = ""
        for col, val in where.items():
            what = '{0} = "{1}"'.format(col, val)
            if not wquery:
                wquery = " where " + what
            else:
                wquery += " and " + what
        rquery = " | reverse()" if reverse else ""
        params = urllib.urlencode({
            'q': query + wquery + rquery,
            'env': 'store://datatables.org/alltableswithkeys',
        })
        url = 'http://query.yahooapis.com/v1/public/yql?' + params
        source = urllib.urlopen(url)
        tree = ElementTree()
        tree.parse(source)
        return tree
        
    #----------------------------------------------------------------------
    def find(self, query):
        result = []
        tree = self._yql('yahoo.finance.quoteslist', {'symbol': query})
        if tree.find('*/quote/LastTradeDate').text:
            result.append(Ticker(self, query))
        return result
            
    #----------------------------------------------------------------------
    def quotes(self, ticker):
        tree = self._yql('yahoo.finance.quotes', {'symbol': ticker.symbol})
        return YahooQuotes(
            {decapitalize(e.tag): e.text for e in tree.find('*/quote')}
        )        

    #----------------------------------------------------------------------
    @staticmethod
    def _generator(ticker, tree, start, end, period):
        """
        Wrap responsed data with CSV parser and return elements in the order.
        """
        for quote in tree.iter("quote"):
            try:
                d = quote.find('Date').text
                timestamp = datetime.strptime(d, "%Y-%m-%d")
                o = float(quote.find('Open').text)
                h = float(quote.find('High').text)
                l = float(quote.find('Low').text)
                c = float(quote.find('Close').text)
                v = int(quote.find('Volume').text)
            except ValueError as ve:
                raise InvalidDataFormatError(ticker)
            yield Bar(ticker, timestamp, period, o, h, l, c, v)
                
    #----------------------------------------------------------------------
    def bars(self, ticker, start, end, period):
        if period != timedelta(days=1):
            raise ValueError("Yahoo retrive daily data only.")
        tree = self._yql('yahoo.finance.historicaldata', {
            'symbol': ticker.symbol,
            'startDate': start.isoformat(),
            'endDate': end.isoformat(),
            }, reverse=True)
        return YahooProvider._generator(ticker, tree, start, end, period)
            