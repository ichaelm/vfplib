'''
Created on Jun 5, 2014

@author: mschaffe
'''

from .graph import Graph
from .ui_structure import Button, FieldButton, Click, NumericalEntry
import random

def merge_buttons(source, target):
    diff = set()
    assert source == target
    if isinstance(source, FieldButton):
        assert isinstance(target, FieldButton)
        for sourcesetting in source.settings:
            if sourcesetting not in target.settings:
                target.settings.add(sourcesetting)
                diff.add(sourcesetting)
        target.set_setting(source.setting)
    return diff

def merge_screens(source, target):
    diffs = {}
    assert(source == target)
    for buttonname in source.buttonmap:
        sourcebutton = source.buttonmap[buttonname]
        targetbutton = target.buttonmap[buttonname]
        diff = merge_buttons(sourcebutton, targetbutton)
        diffs[buttonname] = diff
    return diffs

class Crawler(object):
    def __init__(self, parser):
        self.parser = parser
        self.graph = Graph()
        self.lastfullscreen = None
        self.lastscreen = None
        self.currentscreen = None
        self.currentclick = None

    def click(self, click):
        button = click.button
        setting = click.setting
        if setting:
            assert isinstance(button, FieldButton)
        if self.currentscreen == None:
            raise RuntimeError('Crawler: Must run analyze() before click()')
        if button not in self.currentscreen.buttonmap.values():
            raise RuntimeError('Crawler: Cannot click ' + str(button) + ': not found on current screen')
        if setting:
            if setting not in self.currentscreen.buttonmap[button.name].settings:
                raise RuntimeError('Crawler: Cannot click ' + str(button) + ' with setting ' + str(setting) + ': not found in stored settings')
            if setting != self.currentscreen.buttonmap[button.name].setting:
                raise RuntimeError('Crawler: Cannot click ' + str(button) + ' with setting ' + str(setting) + ': not current setting')
        self.currentclick = click
        self.lastscreen = self.currentscreen
        if self.lastscreen.parent == None:
            self.lastfullscreen = self.lastscreen
        self.parser.click(button)

    def press(self, hardbuttonname):
        self.parser.press(hardbuttonname)
        if hardbuttonname == 'exit':
            self.currentscreen = self.lastscreen

    def analyze(self):
        screen = self.parser.analyze(self.lastfullscreen)
        if isinstance(screen, NumericalEntry):
            buttons = [screen.buttonmap['Cancel']]
        else:
            buttons = screen.buttonmap.values()
        clicks = set()
        for button in buttons:
            if isinstance(button, FieldButton):
                clicks.add(Click(button, button.setting))
            else:
                clicks.add(Click(button))
        if screen not in self.graph:
            self.graph.add(screen, clicks)
        else:
            diffs = merge_screens(screen, self.graph.nodemap[screen].value)
            for buttonname in diffs:
                diff = diffs[buttonname]
                for setting in diff:
                    self.graph.add_edge(screen, Click(screen.buttonmap[buttonname], setting))
        self.currentscreen = screen
        if self.lastscreen != None:
            assert self.currentclick != None
            self.graph.add_edge(self.lastscreen, self.currentclick, self.currentscreen)
        return screen

    def crawl(self):
        self.analyze()
        path = self.graph.nearest_unexplored_edge(self.currentscreen)
        while path:
            for click in path:
                clickedclicks = set(self.graph.explored_edges(self.currentscreen))
                currentclicks = self.currentscreen.get_current_clicks()
                if click not in currentclicks:
                    newclick = Click(self.currentscreen.buttonmap[click.button.name], self.currentscreen.buttonmap[click.button.name].setting)
                    print('want to do ' + str(click) + ' instead doing ' + str(newclick))
                    click = newclick
                self.click(click)
                self.analyze()  # temp
                break  # temp
                if click in clickedclicks:
                    expectedcurrentscreen = self.graph.follow_edge(self.lastscreen, click)
                    self.analyze()
                    break  # temp
                    if self.currentscreen != expectedcurrentscreen:
                        break
                else:
                    self.analyze()
            path = self.graph.nearest_unexplored_edge(self.currentscreen)
        return self.graph

    def goto(self, targetscreen):
        self.analyze()
        path = self.graph.shortest_path(self.currentscreen, targetscreen)
        while path:
            for click in path:
                clickedclicks = set(self.graph.explored_edges(self.currentscreen))
                currentclicks = self.currentscreen.get_current_clicks()
                if click not in currentclicks:
                    newclick = Click(self.currentscreen.buttonmap[click.button.name], self.currentscreen.buttonmap[click.button.name].setting)
                    print('want to do ' + str(click) + ' instead doing ' + str(newclick))
                    click = newclick
                self.click(click)
                self.analyze()  # temp
                break  # temp
                if click in clickedclicks:
                    expectedcurrentscreen = self.graph.follow_edge(self.lastscreen, click)
                    self.analyze()
                    break  # temp
                    if self.currentscreen != expectedcurrentscreen:
                        break
                else:
                    self.analyze()
            path = self.graph.shortest_path(self.currentscreen, targetscreen)

    def __str__(self):
        return 'Crawler on ' + str(self.parser)

