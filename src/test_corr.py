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
		
class testKotirIndexConstructs(unittest.TestCase):
	def setUp(self,):
		pass
	def _testiuok(self,):
		
		assert len(uniqueIndex())

class testCorrOk(unittest.TestCase):
	def setUp(self,):
		pass
	def testCorrelationFunctionWorks(self,):
		n = correlate([],[]); self.assertTrue(n!=n)
		self.assertEqual(correlate([1.0],[1]), 1)
		self.assertEqual(correlate([1.0,0],[0,1]), 0)
		self.assertEqual(correlate([1.0,2,3],[3,2,1]), 10.0/(14*14))
		
		
	def ignoreItTestCorrIgnoresNone(self,):
		self.assertEqual(correlate([None,None,None],[3,None,1]), 0)
		self.assertEqual(correlate([None,2,None],[3,None,1]), 0)
		self.assertEqual(correlate([1,2,None],[3,None,1]), 3/(1*3))
		
	def testDiffererntLengthsCorrelate(self,):
		early = hist_data([1,2,2,2,2,2,2,2,2], start_date = datetime.datetime(2000,1,1))
		late = hist_data([2,2,2,2,2,2,2,2], start_date = datetime.datetime(2000,1,2))
		self.assertEqual(correlate(early,late), 1)
		
		
if __name__ == '__main__':
	unittest.main()
