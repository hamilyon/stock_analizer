#!/usr/bin/env python3
# --* encoding:utf8  *--
# -----------------------------------------------------------------------------
# csvkotir.py
# -----------------------------------------------------------------------------
from di import *
from corlib import *

def get_all_tick(file, ):
	with open(file) as raw_csv:
		dr = csv.DictReader(raw_csv,dialect = excel)
		ticks = []
		for line in dr:
			t = line['TICKER']
			if not t in ticks:
				ticks.append(t)
	return ticks
		
		
		

def filter(next = gsingleton(print__)):
	prev = None
	while True:
		x = yield
		y = yield
		if isinstance(x, float):
			x,y = y,x
		if isinstance(y, float):
			next.send(x )
			
def indicator(next = gsingleton(print__)):

	prev = None
	while True:
		x = yield
		if prev:
			if x/prev > 1.1:
				next.send(x/prev -1 )
		prev = x



def interactive(next = gsingleton(print__)):
	print ' getting EESR ticks printed '
	for t in open_all_ticks(file_with_all,ticks):
		#~ print 'inside'
		for d in t.data:
			next.send( d ) 
			

if __name__ == '':
	# interactive use
	#~ print 'outside'
	interactive()

