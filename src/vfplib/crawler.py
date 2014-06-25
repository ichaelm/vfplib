'''
Created on Jun 5, 2014

@author: mschaffe
'''

from .parser import Parser, Button
from .graph import Graph

class Crawler(object):
    def __init__(self, parser):
        assert isinstance(parser, Parser)
        self.parser = parser
        self.graph = Graph()
        self.lastfullscreen = None

    def click(self, button):
        assert isinstance(button, Button)
        assert hasattr(self, 'currentscreen')
        if button in self.currentscreen.buttons:
            self.currentbutton = button
            self.lastscreen = self.currentscreen
            if self.lastscreen.parent == None:
                self.lastfullscreen = self.lastscreen
            self.parser.click(button)

    def press(self, hardbuttonname):
        assert isinstance(hardbuttonname, str)
        self.parser.press(hardbuttonname)
        if hardbuttonname == 'exit':
            self.currentscreen = self.lastscreen

    def analyze(self):
        screen = self.parser.analyze(self.lastfullscreen)

        self.graph.add(screen, screen.buttons)
        self.currentscreen = screen
        if hasattr(self, 'lastscreen'):
            assert hasattr(self, 'currentbutton')
            self.graph.add_edge(self.lastscreen, self.currentbutton, self.currentscreen)

        return screen

    def crawl(self):
        self.analyze()
        path = self.graph.nearest_unexplored_edge(self.currentscreen)
        while path != None:
            for button in path:
                clickedbuttons = set(self.graph.explored_edges(self.currentscreen))
                self.click(button)
                if button in clickedbuttons:
                    expectedcurrentscreen = self.graph.follow_edge(self.lastscreen, button)
                    self.analyze()
                    if self.currentscreen != expectedcurrentscreen:
                        break
                else:
                    self.analyze()
            path = self.graph.nearest_unexplored_edge(self.currentscreen)
        return self.graph

    def __str__(self):
        return 'Crawler on ' + str(self.parser)

