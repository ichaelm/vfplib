'''
Created on Jun 4, 2014

@author: mschaffe
'''

import unittest

from vfplib.crawler import Crawler
import cPickle as pickle
from testing.dummy_parser import DummyParser, dummyscreenmap

# 'test' or 'real' or 'load'
IP = '134.63.79.71'
LOAD_PATH = 'out.pickle'
SAVE = False
SAVE_PATH = 'out.pickle'

class Test(unittest.TestCase):


    def setUp(self):
        # dut = DummySession()
        interp = Crawler(DummyParser())
        graph = interp.crawl()

        assert len(graph) == len(dummyscreenmap)
        for screen in graph:
            assert dummyscreenmap[screen.title] == screen
            print(str(screen) + ' has buttons:')
            for button in screen.buttonmap.values():
                print('    ' + button.name)
            if len(set(graph.explored_edges(screen))) > 0:
                print('  and points:')
                for edge in graph.explored_edges(screen):
                    assert edge.button == screen.buttonmap[edge.button.name]
                    # assert graph.follow_edge(screen, edge).name == edge.name.partition('_to_')[2]
                    print('    through ' + str(edge) + ' to ' + str(graph.follow_edge(screen, edge)))
        print(str(interp.parser.numscreencaps) + ' total screencaps')
        if SAVE:
            pickle.dump(graph, open(SAVE_PATH, 'wb'), protocol=2)
    def tearDown(self):
        pass


    def testName(self):
        pass

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
