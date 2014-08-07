'''
Created on Jun 10, 2014

@author: mschaffe
'''

from vfplib.crawler import Crawler
from vfplib.parser import Parser
from vfplib.session import Session
import cPickle as pickle

IP = '134.63.79.149'
LOAD_PATH = 'out.pickle'
SAVE = False
SAVE_PATH = 'out.pickle'

if __name__ == '__main__':
        dut = Session(IP)
        interp = Crawler(Parser(dut))
        graph = interp.crawl()
        if graph.fully_explored():
            print('Fully explored')
        else:
            print('INCOMPLETE')
            print('Exploration was blocked by unexpected behavior')
        for screen in graph:
            print(str(screen) + ' has buttons:')
            for button in screen.buttonmap.values():
                print('    ' + button.name)
            if len(set(graph.explored_edges(screen))) > 0:
                print('  and points:')
                for edge in graph.explored_edges(screen):
                    print('    through ' + str(edge) + ' to ' + str(graph.follow_edge(screen, edge)))

        if SAVE:
            pickle.dump(graph, open(SAVE_PATH, 'wb'), protocol=2)
