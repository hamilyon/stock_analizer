
import unittest
import sys, os

pdir = os.path.split(__file__)[0]
pdir = os.path.split(pdir)[0]

sys.path[0:0] = [pdir]

loader = unittest.defaultTestLoader

mainsuite = unittest.TestSuite(loader.discover("coverage", "*_test.py"))

unittest.TextTestRunner(verbosity=2).run(mainsuite)
