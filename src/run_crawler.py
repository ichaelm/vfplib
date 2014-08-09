'''
Created on Jun 10, 2014

@author: mschaffe
'''

from __future__ import print_function

from vfplib.crawler import Crawler
from vfplib.parser import Parser
from vfplib.session import Session
from vfplib.ui_structure import Click, NumericalEntry
import cPickle as pickle
import sys

if len(sys.argv) != 2:
    raise RuntimeError('run_crawler requires an IP address')

IP = sys.argv[1]
LOAD_PATH = ''
SAVE = True
LOAD = False
FINAL = True
SAVE_PATH = ''
EXT = '.pickle'
functions = [
    # 'DC Voltage',
    'DC Current',
    # 'AC Voltage',
    # 'AC Current',
    'Resistance 2W',
    # 'Resistance 4W',
    # 'Temperature',
    # 'Frequency',
    # 'Period',
    'Continuity',
    'Capacitance',
    'Diode',
    'DCV Ratio',
    # 'Digitize Voltage',
    # 'Digitize Current',
]

if __name__ == '__main__':
    dut = Session(IP)
    parser_t = Parser(dut)
    for function in functions:
        interp = Crawler(parser_t)
        if LOAD:
            graph = pickle.load(open(SAVE_PATH + function + ' graph' + EXT, 'rb'))
            interp.graph = graph
        else:
            interp.parser.press('menu')
            interp.parser.select_function(function)
            interp.parser.menu_click('Measure: Settings')
            interp.crawl()
            graph = interp.graph
        if graph.fully_explored():
            print('Fully explored ' + function)
        else:
            print(function + 'INCOMPLETE')
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
            pickle.dump(graph, open(SAVE_PATH + function + ' graph' + EXT, 'wb'), protocol=2)
        data = {}  # dict from screen to (dict from button to helpstring)
        for screen in graph:
            if isinstance(screen, NumericalEntry):
                break
            print('going to ' + str(screen))
            data[screen] = {}
            interp.goto(screen)
            print(interp.currentscreen)
            print(screen)
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
            pickle.dump(data, open(SAVE_PATH + function + ' help' + EXT, 'wb'), protocol=2)

        for screen in data:
            for button in data[screen]:
                print(str(screen) + ' :: ' + str(button) + ' :: ' + str(data[screen][button]))
    if FINAL:
        fout = open(SAVE_PATH + 'help' + '.csv', 'wb')
        print('Parent Screen, Screen, Button, Help Caption', file=fout)
        for function in functions:
            data = pickle.load(open(SAVE_PATH + function + ' help' + EXT, 'rb'))
            for screen in data:
                for button in data[screen]:
                    if screen.parent:
                        print(str(screen.parent.title) + ', ' + str(screen.title) + ', ' + str(button.name) + ', ' + str(data[screen][button]), file=fout)
                    else:
                        print(', ' + str(screen.title) + ', ' + str(button.name) + ', ' + str(data[screen][button]), file=fout)
        fout.close()

