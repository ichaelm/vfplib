'''
Created on Jun 10, 2014

@author: mschaffe
'''

from vfplib.crawler import Crawler
from vfplib.parser import Parser
from vfplib.session import Session
from vfplib.ui_structure import Click, NumericalEntry
import cPickle as pickle

IP = '134.63.78.160'
LOAD_PATH = 'out.pickle'
SAVE = True
LOAD = False
SAVE_PATH = 'out.pickle'

if __name__ == '__main__':
    dut = Session(IP)
    interp = Crawler(Parser(dut))
    if LOAD:
        graph = pickle.load(open(SAVE_PATH, 'rb'))
        interp.graph = graph
        interp.analyze()
    else:
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
    if SAVE and not LOAD:
        pickle.dump(graph, open(SAVE_PATH, 'wb'), protocol=2)
    data = {}  # dict from screen to (dict from button to helpstring)
    for screen in graph:
        if isinstance(screen, NumericalEntry):
            break
        print('going to ' + str(screen))
        data[screen] = {}
        interp.goto(screen)
        print interp.currentscreen
        print screen
        assert interp.currentscreen == screen
        buttons = screen.buttonmap.values()
        for button in buttons:
            print('        TRY: ' + str(screen) + ' :: ' + str(button))
            # make focus on button
            if interp.parser.get_focus() != button:
                interp.click(Click(button))
                interp.goto(screen)
                assert interp.currentscreen == screen
            if interp.parser.get_focus() == button:  # if false, then this button cannot be selected on entry
                # get and store help text
                interp.parser.press('help')
                text = interp.parser.get_help_text()
                data[screen][button] = text
                interp.parser.press('exit')
                print('        DONE: ' + str(screen) + ' :: ' + str(button) + ' :: ' + str(data[screen][button]))
            else:
                print('        FAIL: ' + str(screen) + ' :: ' + str(button))

    if SAVE:
        pickle.dump(data, open(SAVE_PATH + '(2)', 'wb'), protocol=2)

    for screen in data:
        for button in data[screen]:
            print(str(screen) + ' :: ' + str(button) + ' :: ' + str(data[screen][button]))

