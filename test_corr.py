#!/usr/bin/env python3
# --* encoding:utf8  *--
# -----------------------------------------------------------------------------
# test_corr.py
# -----------------------------------------------------------------------------

from  corr import presence
import unittest



class testPresence(unittest.TestCase):
	def setUp(self,):
		print 'setup'
		self.presence = presence()
		pass
	def testNextDayTest(self,):
		cd = self.presence.current_date
		self.presence.next_day.send(1)
		nd = self.presence.current_date
		print cd, nd

if __name__ == '__main__':
	unittest.main()
