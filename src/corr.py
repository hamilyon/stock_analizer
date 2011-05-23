#!/usr/bin/env python3
# --* encoding:utf8  *--
# -----------------------------------------------------------------------------
# corr.py
# -----------------------------------------------------------------------------
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import os.path
import numpy as np
import csv
import pprint
from matplotlib import rc
from itertools import *
from di import singleton, gsingleton
from corlib import *

mappings = []


def uniqueIndex(src, f):
	return map(dl(f),src,)

def iuniqueIndex(src, f):
	return imap(dl(f),src,)

dl = lambda f: lambda x: [x, f(x)]



#def storeTo(mappings):
#	mappings.append(yield)

files_csv = '''/home/hamilyon/Downloads/HYDR_991001_101121.txt
/home/hamilyon/Downloads/SNGS_991001_101121.txt
/home/hamilyon/Downloads/SBER_991001_101121.txt
/home/hamilyon/Downloads/MTLR_991001_101121.txt
/home/hamilyon/Downloads/LKOH_991001_101121.txt
/home/hamilyon/Downloads/GAZP_991001_101121(2).txt
/home/hamilyon/Downloads/VTBR_991001_101121.txt
/home/hamilyon/Downloads/AFLT_991001_101121.txt
/home/hamilyon/Downloads/AVAZ_991001_101121.txt
/home/hamilyon/Downloads/ARMD_991001_101121.txt
/home/hamilyon/Downloads/SCOH_991001_101121.txt
/home/hamilyon/Downloads/MSNG_991001_101121.txt
/home/hamilyon/Downloads/GAZP_991001_101121.txt'''

files_csv = '''/home/hamilyon/Downloads/SNGS_991001_101121.txt
/home/hamilyon/Downloads/SBER_991001_101121.txt
/home/hamilyon/Downloads/LKOH_991001_101121.txt
/home/hamilyon/Downloads/GAZP_991001_101121(2).txt
/home/hamilyon/Downloads/VTBR_991001_101121.txt
/home/hamilyon/Downloads/AFLT_991001_101121.txt
/home/hamilyon/Downloads/AVAZ_991001_101121.txt
/home/hamilyon/Downloads/SCOH_991001_101121.txt
/home/hamilyon/Downloads/MSNG_991001_101121.txt
/home/hamilyon/Downloads/GAZP_991001_101121.txt'''

files_csv = files_csv.split()

file_with_all = 'ALL_TICKERS.csv'

with open('resource/ticks') as f:
	ticks = f.read().split()

ticks = ['EESR',]

class hist_data():
	def __init__(self, data = None, name = None, lenth = None, start_date = None, end_date = None):
		(self.data, self.name, self.lenth, self.start_date, self.end_date, ) = data, name, lenth, start_date, end_date
		tick = datetime.timedelta(1)
		pass
	def __str__(self,):
		return unicode(self,)
	def __unicode__(self,):
		#~ print self.data
		data = ''
		if None != self.data: data = str(self.data)
		return '<' + str(self.__class__) + (self.name or ' ? ') + (data) + '>'
	pass

class percent(hist_data):
	def __str__(self):
		return super.__str__(self)
		
	def __unicode__(self):
		return super.__unicode__(self)
	pass

class excel(csv.Dialect):
    delimiter = ','
    quotechar = '"'
    escapechar = None
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL

def present(dr, tick = datetime.datetime(1998,02,03)):
	''' present(dr, tick) -> presence of ticker in dr, where dr is csv historical data, presence is object with start_date optional date (dafaults to datetime.datetime(1998,02,03)) )'''

class presence():
	def __init__(self, start_date= datetime.datetime(1998,02,03)):
		self.start_date = start_date
		self.i = 0
		self.current_date = start_date
		self.from_ = 0
		self.to = -1
	
	def next_day(self,):
		while True:
			day = yield 
			if day:
				#self.i = self.i +1
				self.current_date = self.current_date + datetime.timedelta(1)
				#self.to = self.i
	
	def got_cotir(self, ):
		while True:
			t = yield
			if t:
				if not self.from_:
					self.from_ = self.current_date
				self.to = self.current_date
				
def get_col_name(dr, nm = 'TICKER'):
	#print dir(dr)
	#print dr.__iter__().next().keys()
	return 'TICKER'
	
def float_or_zero(string):
	try: 
		return float(string)
	except ValueError, e:
		return 0
def open_csv_kotir(file, tick = None):
	if tick:
		with open(file) as raw_csv:
			dr = csv.DictReader(raw_csv,dialect = excel)
			col = get_col_name(dr)
			print tick
			#print dr.__iter__().next()
			#tick = None
			arr = [[float_or_zero(line['OPEN']),float_or_zero(line['HIGH']),float_or_zero(line['LOW']),float_or_zero(line['CLOSE'])] for line in dr if line['TICKER'] == tick]
			#present = [line['TICKER'] == tick for line in dr]
			
			#start = present.index(1)
			#present =  Present()
			#end = len(present) + start
			
			lenth = len(arr)
			
			arr = np.array(arr)
		return hist_data(arr, tick, lenth)

	#tick = file[25:29] 
	with open(file) as raw_csv:
		dr = csv.DictReader(raw_csv,dialect = excel)
		tick = None
		for line in dr:
			tick = tick or line['<TICKER>']
			#print tick
			break
		arr = [[float(line['<OPEN>']),float(line['<HIGH>']),float(line['<LOW>']),float(line['<CLOSE>'])] for line in dr]
		arr = np.array(arr)
	return hist_data(arr, tick)

def open_all_files(files):
	all_kotir = [open_csv_kotir(file) for file in files]
	return all_kotir

def open_all_ticks(file_with_all, ticks):
	all_kotir = [open_csv_kotir(file_with_all, tick) for tick in ticks]
	return all_kotir

def determine_percent(hist):
	''' determine_percent(arr) -> np.array() with shape (n-1,) where n is length of initial array and elements are percent delta to previous day'''
	arr = hist.data
	arr_2 = np.copy(arr)
	#print arr[:,3]
	d =  (arr[1:,3] - arr[:-1,3])/arr[:-1,3]  # np.array((0,0,0,0)))
	#print hist.name, d
	pc = percent()
	pc.name = hist.name
	pc.data = d
	return pc
	
def determine_all_percent(hist_kotir):
	return [determine_percent(hist_kotir) for hist_kotir in hist_kotir  ]
	
def correlation(hist_kotir):
	pc = determine_all_percent(hist_kotir)
	print [p.data.shape for p in pc]
	# sum() is add.reduce()
	trim = min([p.data.shape for p in pc])[0]
	#i = pc.__iter__()
	#p1 = i.next()
	#p2 = i.next()
	#print 'shape1', p1.data[-460:].shape
	#print 'shape2', p2.data[-460:].shape
	#x = sum(p1.data[:-460]*p2.data[:-460]) 
	return [ [  sum(p1.data[-trim :]*p2.data[-trim :])  for p2 in pc ] for p1 in pc ]
	
	
def matrixmin(mx, n = 1):
	if n!= 1:
		raise Exception('Not implemented jet')
	print np.array(mx).argmin(1)
	return np.array(mx).argmin(0)
	
def get_range_with_full_tickers():
	all_kotir = open_al_csv_kotir()

def xor(a,b):
	return (a and b) or (not a and not b)

def normalize(a,b):
	drift = (a.start_date - b.start_date).days
	return 

def correlate(a,b):
	
	if xor(hasattr(a,'data'), hasattr(b,'data')):
		raise ValueError()
	if hasattr(a,'data'): 
		a,b = normalize(a,b)
	return np.dot(a,b)/(np.dot(a,a)*np.dot(b,b))

if __name__ == '__main__':
	import sys
	if len(sys.argv)==2 and sys.argv[1] == '-t':
		for i in get_all_tick(file_with_all):
			print i
	elif len(sys.argv)==2 and sys.argv[1] == '-r':
		print get_range_with_full_tickers()
	elif len(sys.argv)==2 and sys.argv[1] == '-p':   
		hist_kotir = open_all_ticks(file_with_all,ticks)
		import pickle
		[pickle.dump(x,open('./pdata/'+x.name,'w')) for x in hist_kotir]
	elif len(sys.argv)==2 and sys.argv[1] == '-db':   
		hist_kotir = open_all_ticks(file_with_all,ticks)
		db = connect('./pdata/database')
		[db.execute() for x in hist_kotir]
		[pickle.dump(x,open('./pdata/'+x.name,'w')) for x in hist_kotir]
		
	else:
		
		hist_kotir = open_all_files(files_csv)
		hist_kotir = open_all_ticks(file_with_all,ticks)
		#determine_percent(all_kotir[0])
		crln = correlation(hist_kotir)
		#pprint.pprint( crln )
		print matrixmin(crln)
	
	
		pprint.pprint( [kotir.name for kotir in hist_kotir] )
		
# результат ARMD, HYDR
# из древних AVAZ, SCOH

