'''
Created on Jun 4, 2014

@author: mschaffe
'''

import unittest

from vfplib.crawler import Crawler
import cPickle as pickle
from testing.dummy_parser import DummyParser, dummyscreenmap

verbose = False

class Test(unittest.TestCase):

    def iteration(self):
        # dut = DummySession()
        interp = Crawler(DummyParser())
        graph = interp.crawl()

        assert len(graph) == len(dummyscreenmap)
        for screen in graph:
            assert dummyscreenmap[screen.title] == screen
            if verbose:
                print(str(screen) + ' has buttons:')
                for button in screen.buttonmap.values():
                    print('    ' + button.name)
            if len(set(graph.explored_edges(screen))) > 0:
                if verbose:
                    print('  and points:')
                for edge in graph.explored_edges(screen):
                    assert edge.button == screen.buttonmap[edge.button.name]
                    # assert graph.follow_edge(screen, edge).name == edge.name.partition('_to_')[2]
                    if verbose:
                        print('    through ' + str(edge) + ' to ' + str(graph.follow_edge(screen, edge)))
        if verbose:
            print(str(interp.parser.numscreencaps) + ' total screencaps')

    def testIterations(self):
        for i in xrange(1000):
            if verbose:
                print('ITERATION ' + str(i))
            self.iteration()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
