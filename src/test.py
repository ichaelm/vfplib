'''
Created on Jun 21, 2014

@author: Michael
'''

import unittest
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testing.test_parser'))
unittest.TextTestRunner(verbosity=2).run(suite)
