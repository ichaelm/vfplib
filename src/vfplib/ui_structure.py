"""
Defines the classes and constants that define the structural components of the
device's UI. Instances of these classes are built by the parser and returned to
the crawler.

Created on Jun 10, 2014

@author: mschaffe
"""

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
    """Represents a button on a particular screen.  Immutable.

    The unique identity of a button is determined by its name and coordinates,
    and is only valid among other buttons on the same screen. Whenever a button
    object is hashed, that hash is guaranteed not to collide with other buttons
    on the same screen, but there is no guarantee about buttons on different
    screens.

    Attributes:
        name (str): The button's name on the screen, either as a label or as
        text inside the button.
        coord (tuple of int): The button's coordinates on the screen, ideally
        the center.

    """
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
    """Represents a field-setting button on a particular screen.  Immutable.

    Note that the unique identity of a field button is determined only by its
    name and coordinates, just like a normal button. The setting can change
    without affecting the hash value or equality of the field button.

    Attributes:
        name (str): The button's name on the screen, as a label. Inherited
        from Button.
        coord (tuple of int): The button's coordinates on the screen, ideally
        the center. Inherited from Button.
        setting (str): The button's current setting, as text inside the button.

    """
    def __init__(self, name, coord, setting):
        super(FieldButton, self).__init__(name, coord)
        self.setting = setting

    def __str__(self):
        return 'FieldButton: ' + str(self.name)

class Screen(object):
    """Represents a screen in the UI, either a full screen or a popup screen.
    Immutable.

    The unique identity of a screen is determined by its title, its set of
    buttons, and its parent screen, if any.

    Note that although the equality contract of Button uses both the button's
    name and its coordinates, Screen's buttonmap attribute makes the
    assumption that all buttons have a unique name.

    Attributes:
        title (str): The screen's title, generally at the top of the screen.
        buttonmap (dict): The screen's mapping of button names to buttons.
        parent (Screen): The screen's parent screen. This attribute is currently
        used to store the full screen from which a popup screen is spawned.
        Optional.

    """
    def __init__(self, title, buttons, parent=None):
        self.title = title
        self.buttonmap = {}
        for button in buttons:
            self.buttonmap[button.name] = button
        self.parent = parent

    def __hash__(self):
        return hash((self.title, frozenset(self.buttonmap.values()), self.parent))

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
    """Represents a numerical entry screen in the UI. Immutable.

    All numerical entry screens have the exact same buttonmap, derived from
    NUMERICAL_ENTRY_BUTTONS.

    Attributes:
        title (str): The numerical entry screen's title. Inherited from
        Screen.
        buttonmap (dict): The screen's mapping of button names to buttons.
        Same for all numerical entry screens.
        parent (Screen): The numerical entry screen's parent screen. This
        attribute is currently used to store the full screen from which this
        screen is spawned as a popup. Optional.

    """

    NUMERICAL_ENTRY_BUTTONS = []
    for name in NUMERICAL_ENTRY_MAP:
        coord = NUMERICAL_ENTRY_MAP[name]
        NUMERICAL_ENTRY_BUTTONS.append(Button(name, coord))

    def __init__(self, title, parent=None):
        super(NumericalEntry, self).__init__(title, self.NUMERICAL_ENTRY_BUTTONS, parent)

    def __str__(self):
        return 'NumericalEntry: ' + str(self.title)
