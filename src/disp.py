#!/usr/bin/env python3
# --* encoding:utf8  *--
# -----------------------------------------------------------------------------
# disp.py
# -----------------------------------------------------------------------------


import unittest
import numpy as np
import random


def threshhold(arr, thresh= None)
	if not thresh:
		thresh = np.sort(arr)

def integral(arr, ):
	result = 0.0
	for row in arr:
		for cell in row:
			result += cell
			
def threshhold(arr, thresh= None)
	if not thresh is None:
		thresh = integral(arr)/len(arr)**2
	result  = []
	for row in arr:
		result.append([x for cell in row if cell<thresh else 0])
				
				
class testDispMin(unittest.TestCase):
	def setUp(self,):
		self.data1 = np.array([0,0,0,1,1,1,0,2,2,2,10,10,10,10])/10.0
		
	def testGetGroups(self, ):
		symmatrix = []
		for i in range(len(self.data1):
			shuffle(self.data1)
			reasult.append(self.data1)
		for i in range(len(symmatrix)):
			for j in range(i):
				symmatrix[i][j] = symmatrix[j][i]
		# assert symmatrix is symetrical matrix
		
		
if __name__ == '__main__':
	unittest.main()

