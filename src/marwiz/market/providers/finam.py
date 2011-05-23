"""
This module contains FinamProvider which automatically load data from finam.ru web site.
"""

import urllib, urllib2, re, csv
from datetime import datetime, timedelta
from .base import DataProvider, Ticker, DataFetchingError, DataNotFoundError, InvalidDataFormatError
from market.data import *

__all__ = ["FinamProvider"]

# Download once whel module is importing
# Get a file-like object for the Python Web site's home page.
f = urllib.urlopen("http://www.finam.ru/scripts/export.js")
# Read from the object, storing the page's contents in 's'.
lines = f.readlines()    
            
# Don't use 'eval'. Cause it's dangerous!
def parsetuple(s, trans=str):
    s = s.strip(" \t()")
    return [trans(val) for val in s.split(",")]

# Parse all string in export.js
for line in lines:
    m = re.match(r"var\s+(\w+)\s*=\s*new\s+Array\s*(.*);", line)
    varname = m.group(1)
    varval = m.group(2)
    if varname == "aEmitentIds":
        aEmitentIds = parsetuple(varval, int)
    elif varname == "aEmitentCodes":
        aEmitentCodes = parsetuple(varval.replace("'", ""))
    elif varname == "aEmitentMarkets":
        aEmitentMarkets = parsetuple(varval, int)
        
# Split codes and ids into pairs
pairs = zip(aEmitentMarkets, aEmitentIds)
DATABASE = dict(zip(aEmitentCodes, pairs))

resolutions = {
    timedelta(minutes=1):  2,
    timedelta(minutes=5):  3,
    timedelta(minutes=10): 4,
    timedelta(minutes=15): 5,
    timedelta(minutes=30): 6,
    timedelta(hours=1):    7,
    timedelta(days=1):     8,
    timedelta(weeks=1):    9,
}

########################################################################
class FinamProvider(DataProvider):
    """
    Loads data from finam.ru and cache results in csv files.
    """

    #----------------------------------------------------------------------
    def _generator(self, ticker, lines, start, end, period):
        """
        Wrap responsed data with CSV parser and return elements in the order.
        """
        for datalist in csv.reader(lines, delimiter=';'):
            try:
                d, t, o, h, l, c, v = datalist
                o, h, l, c, v = float(o), float(h), float(l), float(c), int(v)
                stamp = datetime.strptime(d + t, "%Y%m%d%H%M%S")
            except ValueError as ve:
                raise InvalidDataFormatError(ticker, str(datalist))
            if stamp < start:
                continue
            elif stamp > end:
                raise StopIteration
            yield Bar(ticker, stamp, period, o, h, l, c, v)

    #----------------------------------------------------------------------
    def find(self, query):
        result = []
        for i, code in enumerate(aEmitentCodes):
            if query == code:
                result.append(Ticker(self, code, market=aEmitentMarkets[i], id=aEmitentIds[i]))
        if not result:
            raise DataNotFoundError("Not found tickers for " + query)
        return result
            
    #----------------------------------------------------------------------
    def bars(self, ticker, start, end, period):
        """
        Finds ticker in the finam's database stored in export.js file which parsed before
        and trying to find data in a cache or if not download data from a remote service
        and save into cache for further using.
        """
        fmt = "%y%m%d" # Date format of request
        dfrom = start.date()
        dto = end.date()
        fname = "{0}_{1}_{2}".format(ticker.symbol, dfrom.strftime(fmt), dto.strftime(fmt))
        fext = ".csv"
        # Resolution
        try:
            p = resolutions[period]
        except KeyError:
            raise ValueError("Illegal value of period.")
        # Load file from finam if haven't ever loaded
        rdict = dict(d='d',
                     market=ticker.data['market'],
                     cn=ticker.symbol,
                     em=ticker.data['id'],
                     p=p,
                     yf=dfrom.year,
                     mf=dfrom.month-1, # In service month's numbers starts from 0
                     df=dfrom.day,
                     yt=dto.year,
                     mt=dto.month-1,
                     dt=dto.day,
                     dtf=1,  # Equals %Y%m%d
                     tmf=1,  # Equals %M%H%S
                     MSOR=0, # Begin of candles
                     sep=3,  # Semicolon ';'
                     sep2=1, # Not set a digit position delimiter
                     datf=5, # Format: DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL
                     f=fname,
                     e=fext,
                     at=0, # No header
                     )
        
        # The approach below DON'T WORK ((( Service is sensitive to an order of parameters!
        # gets = urllib.urlencode(rdict)
        # url = "http://195.128.78.52/{0}{1}?{2}".format(fname, fext, gets)
        # Stupid way to build an url...
        url = ("http://195.128.78.52/{f}{e}?" + 
              "d=d&market={market}&em={em}&df={df}&" + 
              "mf={mf}&yf={yf}&dt={dt}&mt={mt}&yt={yt}&" + 
              "p={p}&f={f}&e={e}&cn={cn}&dtf={dtf}&tmf={tmf}&" +
              "MSOR={MSOR}&sep={sep}&sep2={sep2}&datf={datf}&at={at}").format(**rdict)
        req = urllib2.Request(url)
        req.add_header('Referer', "http://www.finam.ru/analysis/export/default.asp")
        try:
            resp = urllib2.urlopen(req)
            return self._generator(ticker, resp, start, end, period) # Return generator which parses data
        
        except urllib2.URLError as urle:
            raise DataFetchingError(ticker, urle)
