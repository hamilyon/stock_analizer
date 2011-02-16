#!/usr/bin/env python3
# --* encoding:utf8  *--
# -----------------------------------------------------------------------------
# test_corr.py
# -----------------------------------------------------------------------------

from  corr import *
import unittest



class testPresence(unittest.TestCase):
	def setUp(self,):
		self.presence = presence()
		pass
	def testNextDayTest(self,):
		cd = self.presence.current_date
		nd = self.presence.next_day(); nd.send(None)
		nd.send(1)
		#self.presence.next_day()
		nd = self.presence.current_date
		self.assertEqual( (cd - nd).days ,-1)
	def testCotirOk(self,):

		cd = self.presence.current_date
		nd = self.presence.next_day(); nd.send(None)
		gc = self.presence.got_cotir(); gc.send(None)
		nd.send(1)
		nd.send(1)
		nd.send(1)
		gc.send(1)
		nd.send(1)
		nd.send(1)
		nd.send(1)
		gc.send(1)
		nd.send(1)
		nd.send(1)
		nd.send(1)
		nd = self.presence.current_date
		self.assertEqual( (cd - nd).days ,-9)
		self.assertEqual ((self.presence.from_ - self.presence.to).days ,-3)


class testUIndex(unittest.TestCase):
	def setUp(self,):
		pass
	def testuitrivial(self,):
		assert [['s', 'S'], ['t', 'T'], ['l', 'L']] == uniqueIndex( 'stl', str.upper,)
		
class testKotirIndexConstructsunittest.TestCase):
	def setUp(self,):
		pass
	def testiuok(self,):
		
		assert len(uniqueIndex())
		
if __name__ == '__main__':
	unittest.main()
