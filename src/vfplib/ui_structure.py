'''
Created on Jun 10, 2014

@author: mschaffe
'''

from .hashset import FrozenHashSet

NUMERICAL_ENTRY_MAP = {  # '1'      : (228,341),
                       # '2'      : (311,341),
                       # '3'      : (394,341),
                       # '4'      : (228,258),
                       # '5'      : (311,258),
                       # '6'      : (394,258),
                       # '7'      : (228,175),
                       # '8'      : (311,175),
                       # '9'      : (394,175),
                       # '0'      : (228,424),
                       # '+/-'    : (311,424),
                       # '.'      : (394,424),
                       # 'Clear'  : (560,258),
                       # 'OK'     : (669,341),
                       'Cancel' : (669, 424)
}

class Button(object):
    #immutable!!!
    # name
    # coordinates
    # pointer to target screen
    def __init__(self, name, coord):
        assert isinstance(name, str)
        assert isinstance(coord, tuple)
        assert len(coord) == 2
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
        return 'Button: ' + self.name

class FieldButton(Button):
    def __init__(self, name, coord, setting):
        super(FieldButton, self).__init__(name, coord)
        self.setting = setting

    def __str__(self):
        return 'FieldButton: ' + self.name

NUMERICAL_ENTRY_BUTTONS = []
for name in NUMERICAL_ENTRY_MAP:
    coord = NUMERICAL_ENTRY_MAP[name]
    NUMERICAL_ENTRY_BUTTONS.append(Button(name, coord))

NUMERICAL_ENTRY_BUTTONS_MAP = {}
for button in NUMERICAL_ENTRY_BUTTONS:
    NUMERICAL_ENTRY_BUTTONS_MAP[button.name] = button

class Screen(object):
    """ Represents an immutable and unique UI screen.

    Stores the screen's name as a string, and all of its buttons as Button objects.
    Uniqueness is determined by the name and set of buttons

    NEW: stores mutable settings that are NOT hashed
    """
    def __init__(self, name, buttons):
        assert isinstance(name, str)
        self.name = name
        self.buttons = FrozenHashSet(buttons)
        for button in self.buttons:
            assert isinstance(button, Button)

    def __hash__(self):
        return hash((self.name, self.buttons))

    def __eq__(self, other):
        if isinstance(other, Screen):
            return (self.name, self.buttons) == (other.name, other.buttons)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Screen: ' + self.name

class SubScreen(Screen):
    """ Represents an immutable and unique UI screen that is actually just a popup screen accessible only through a parent screen.

    In addition to Screen's name and buttons fields, this also stores the parent screen as a Screen object.
    Uniqueness is determined by the name, set of buttons, and parent screen.
    """
    def __init__(self, name, buttons, parent=None):
        assert (parent == None) or isinstance(parent, Screen)
        super(SubScreen, self).__init__(name, buttons)
        self.parent = parent

    def __hash__(self):
        return hash((self.name, self.buttons, self.parent))

    def __eq__(self, other):
        if isinstance(other, SubScreen):
            return (self.name, self.buttons, self.parent) == (other.name, other.buttons, other.parent)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'SubScreen: ' + self.name + ', child of ' + str(self.parent)

class NumericalEntry(SubScreen):
    def __init__(self, name, parent=None):
        super(NumericalEntry, self).__init__(name, NUMERICAL_ENTRY_BUTTONS, parent)

    def __str__(self):
        return 'NumericalEntry: ' + self.name
