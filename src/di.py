#!/usr/bin/env python3
# --* encoding:utf8  *--
# -----------------------------------------------------------------------------
# di.py
# -----------------------------------------------------------------------------


# rl framework



idx = {'__pack__name__':lambda x: x.__name__
	}

def pack(x):
	idx[x.__name__] = x
	return x
	
@pack
def f(x,y,z):
	return x
	
def loc(name):
	return idx[name]
	
if __name__ == '__main__':
	print f(1,2,3)
	print loc('f')(2,3,4)
#/ rl framework


# di framework
sgts = {}
def singleton(x):
	if x == None:
		raise ValueError("'None' factory is not permitted")
	if sgts.get(x, None) == None:
		sgts[x] = x()
	return sgts[x]
	
#def isingleton(x):

sgts = {}
def gsingleton(x):
	if x == None:
		raise ValueError("'None' factory is not permitted")
	if sgts.get(x, None) == None:
		sgts[x] = x()
		sgts[x].send(None)
	return sgts[x]
	

#def iloc():
#	if idx[name]

#def it(x):
#	clazz = loc(x)
	


#
