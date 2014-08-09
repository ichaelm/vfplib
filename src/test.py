'''
Created on Jun 21, 2014

@author: Michael
'''

import unittest
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testing.test_parser'))
suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testing.test_crawler'))
suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testing.test_ui_structure'))
suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testing.test_graph'))
suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testing.test_parser_blackbox'))
suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testing.test_crawler_blackbox'))
unittest.TextTestRunner(verbosity=2).run(suite)
