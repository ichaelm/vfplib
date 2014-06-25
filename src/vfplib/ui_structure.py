'''
Created on Jun 10, 2014

@author: mschaffe
'''

NUMERICAL_ENTRY_MAP = {
    '1'      : (228, 341),
    '2'      : (311, 341),
    '3'      : (394, 341),
    '4'      : (228, 258),
    '5'      : (311, 258),
    '6'      : (394, 258),
    '7'      : (228, 175),
    '8'      : (311, 175),
    '9'      : (394, 175),
    '0'      : (228, 424),
    '+/-'    : (311, 424),
    '.'      : (394, 424),
    'Clear'  : (560, 258),
    'OK'     : (669, 341),
    'Cancel' : (669, 424)
}

class Button(object):
    #immutable!!!
    # name
    # coordinates
    # pointer to target screen
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord

    def __hash__(self):
        return hash((self.name, self.coord))

    def __eq__(self, other):
        if isinstance(other, Button):
            return (self.name, self.coord) == (other.name, other.coord)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Button: ' + str(self.name)

class FieldButton(Button):
    def __init__(self, name, coord, setting):
        super(FieldButton, self).__init__(name, coord)
        self.setting = setting

    def __str__(self):
        return 'FieldButton: ' + str(self.name)

class Screen(object):
    """ Represents an immutable and unique UI screen.

    Stores the screen's name as a string, and all of its buttons as Button objects.
    Uniqueness is determined by the name and set of buttons

    NEW: stores mutable settings that are NOT hashed
    """
    def __init__(self, title, buttons, parent=None):
        self.title = title
        self.buttonmap = {}
        for button in buttons:
            self.buttonmap[button.name] = button
        self.parent = parent

    def __hash__(self):
        return hash((self.title, frozenset(self.buttonmap), self.parent))

    def __eq__(self, other):
        if isinstance(other, Screen):
            return (self.title, self.buttonmap, self.parent) == (other.title, other.buttonmap, other.parent)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        mystr = 'Screen: ' + str(self.title)
        if self.parent != None:
            mystr += ' (child of ' + str(self.parent) + ')'
        return mystr

class NumericalEntry(Screen):

    NUMERICAL_ENTRY_BUTTONS = []
    for name in NUMERICAL_ENTRY_MAP:
        coord = NUMERICAL_ENTRY_MAP[name]
        NUMERICAL_ENTRY_BUTTONS.append(Button(name, coord))

    def __init__(self, title, parent=None):
        super(NumericalEntry, self).__init__(title, self.NUMERICAL_ENTRY_BUTTONS, parent)

    def __str__(self):
        return 'NumericalEntry: ' + str(self.title)
