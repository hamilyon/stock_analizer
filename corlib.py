#!/usr/bin/env python3
# --* encoding:utf8  *--
# -----------------------------------------------------------------------------
# corlib.py
# -----------------------------------------------------------------------------
''' coro utine library '''

def print__():
	while True:
		x = yield
		print x

def wc(next = ):
	while True:
		x = yield	