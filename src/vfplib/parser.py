'''
Created on Jun 4, 2014

@author: mschaffe
'''

import pytesser

from .ui_structure import Button, Screen, NumericalEntry, FieldButton

from .improc import threshold_image, find_subimage
import templates

HARD_BUTTONS = {
    'home'     : 1,
    'menu'     : 2,
    'quickset' : 3,
    'help'     : 4,
    'enter'    : 5,
    'exit'     : 6,
    'function' : 7,
    'trigger'  : 8
}

MAIN_MENU_MAP = {
    'Measure: QuickSet'     : (95, 75),
    'Measure: Settings'     : (95, 163),
    'Measure: Calculations' : (95, 251),
    'Measure: Config List'  : (95, 339),
    'Measure: Data Buffers' : (95, 427),
    'Views: Graph'          : (315, 75),
    'Views: Histogram'      : (315, 163),
    'Views: Sheet'          : (315, 251),
    'Trigger: Templates'    : (450, 75),
    'Trigger: Configure'    : (450, 163),
    'Scripts: Run'          : (585, 75),
    'Scripts: Manage'       : (585, 163),
    'Scripts: Create Setup' : (585, 251),
    'Scripts: Record'       : (585, 339),
    'System: Event Log'     : (720, 75),
    'System: Communication' : (720, 163),
    'System: Settings'      : (720, 251),
    'System: Calibration'   : (720, 339),
    'System: Info/Manage'   : (720, 427)
}

SET_FUNCTION_MEASURE_MAP = {
    'DC Voltage'       : (175, 110),
    'DC Current'       : (400, 110),
    'AC Voltage'       : (175, 170),
    'AC Current'       : (400, 170),
    'Resistance 2W'    : (615, 110),
    'Resistance 4W'    : (615, 170),
    'Temperature'      : (175, 230),
    'Frequency'        : (400, 230),
    'Period'           : (615, 230),
    'Continuity'       : (175, 290),
    'Capacitance'      : (400, 290),
    'Diode'            : (615, 290),
    'DCV Ratio'        : (175, 350),
}

SET_FUNCTION_DIGITIZE_MAP = {
    'Digitize Voltage' : (200, 110),
    'Digitize Current' : (200, 170),
}

SET_FUNCTION_MEASURE_TAB = (200, 40)
SET_FUNCTION_DIGITIZE_TAB = (520, 40)

# ocr
def OCR_image(im):
    text = pytesser.image_to_string(im).replace('\n', ' ').strip(' ')
    return text

# cornerbox processing

def match_corners(ULcorners, URcorners, LLcorners, LRcorners, radius=0):
    quads = []
    for ULcorner in ULcorners:
        URcorner = None
        LLcorner = None
        LRcorner = None
        for prospect in URcorners:
            if prospect[1] >= ULcorner[1] - radius and prospect[1] <= ULcorner[1] + radius and prospect[0] > ULcorner[0] and (URcorner == None or prospect[0] < URcorner[0]):
                URcorner = prospect
        if URcorner == None: continue
        for prospect in LLcorners:
            if prospect[0] >= ULcorner[0] - radius and prospect[0] <= ULcorner[0] + radius and prospect[1] > ULcorner[1] and (LLcorner == None or prospect[1] < LLcorner[1]):
                LLcorner = prospect
        if LLcorner == None: continue
        for prospect in LRcorners:
            if prospect[0] >= URcorner[0] - radius and prospect[0] <= URcorner[0] + radius and prospect[1] >= LLcorner[1] - radius and prospect[1] <= LLcorner[1] + radius:
                LRcorner = prospect
        if LRcorner == None: continue
        quads.append((ULcorner, URcorner, LLcorner, LRcorner))
    return quads

def quad_to_box(quad):
    left = max(quad[0][0], quad[2][0])
    upper = max(quad[0][1], quad[1][1])
    right = min(quad[1][0], quad[3][0])
    lower = min(quad[2][1], quad[3][1])
    return (left, upper, right, lower)

def box_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])

def shrink_box(box, margin):
    left = box[0] + margin
    upper = box[1] + margin
    right = box[2] - margin
    lower = box[3] - margin
    return (left, upper, right, lower)

def adjust_box(box):
    left = box[0] + 4
    upper = box[1] + 4
    right = box[2]
    lower = box[3]
    return (left, upper, right, lower)

def box_to_label_box(box):
    lower = box[1] + 33
    right = box[0] - 5
    upper = lower - 51
    left = right - 220
    return (left, upper, right, lower)

def box_to_label_finding_box(box):
    lower = box[1] + 33
    right = box[0]
    upper = lower - 35
    left = right - 20
    return (left, upper, right, lower)

def fit_box_inside_bounds(box, boundingbox):
    left = max(box[0], boundingbox[0])
    upper = max(box[1], boundingbox[1])
    right = min(box[2], boundingbox[2])
    lower = min(box[3], boundingbox[3])
    return (left, upper, right, lower)

def get_title_box(popupbox=None):
    if popupbox != None:
        titlebox = popupbox
        titlebox = (titlebox[0], titlebox[1], titlebox[2], titlebox[1] + 50)
    else:
        titlebox = (0, 0, 799, 43)  # magicnumber
    return titlebox

def box_center(box):
    return ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)

# higher level
def get_popup_box(screen):
    ULpopupcorners = find_subimage(screen, templates.popup.UL)
    URpopupcorners = find_subimage(screen, templates.popup.UR)
    LLpopupcorners = find_subimage(screen, templates.popup.LL)
    LRpopupcorners = find_subimage(screen, templates.popup.LR)
    popup = len(ULpopupcorners)
    assert popup == len(URpopupcorners) and popup == len(LLpopupcorners) and popup == len(LRpopupcorners)
    if popup > 0:
        popupquads = match_corners(ULpopupcorners, URpopupcorners, LLpopupcorners, LRpopupcorners)
        minarea = 99999999
        for quad in popupquads:
            box = quad_to_box(quad)
            area = box_area(box)
            if area < minarea:
                minarea = area
                popupbox = box
        popupbox = adjust_box(popupbox)
        popupbox = shrink_box(popupbox, 5)
        return popupbox
    else:
        return None

def get_button_boxes(screen, popupbox=None):
    popup = (popupbox != None)
    if popup:
        ULcorners = find_subimage(screen, templates.popupButton.UL, popupbox)
        URcorners = find_subimage(screen, templates.popupButton.UR, popupbox)
        LLcorners = find_subimage(screen, templates.popupButton.LL, popupbox)
        LRcorners = find_subimage(screen, templates.popupButton.LR, popupbox)
        ULcorners += find_subimage(screen, templates.popupButtonSelected.UL, popupbox)
        URcorners += find_subimage(screen, templates.popupButtonSelected.UR, popupbox)
        LLcorners += find_subimage(screen, templates.popupButtonSelected.LL, popupbox)
        LRcorners += find_subimage(screen, templates.popupButtonSelected.LR, popupbox)
    else:
        ULcorners = find_subimage(screen, templates.button.UL)
        URcorners = find_subimage(screen, templates.button.UR)
        LLcorners = find_subimage(screen, templates.button.LL)
        LRcorners = find_subimage(screen, templates.button.LR)
        ULcorners += find_subimage(screen, templates.buttonSelected.UL)
        URcorners += find_subimage(screen, templates.buttonSelected.UR)
        LLcorners += find_subimage(screen, templates.buttonSelected.LL)
        LRcorners += find_subimage(screen, templates.buttonSelected.LR)
    quads = match_corners(ULcorners, URcorners, LLcorners, LRcorners)
    boxes = []
    for quad in quads:
        box = quad_to_box(quad)
        box = adjust_box(box)
        boxes.append(box)
    return boxes

def get_selected_button_boxes(screen, popupbox=None):
    popup = (popupbox != None)
    if popup:
        ULcorners = find_subimage(screen, templates.popupButtonSelected.UL, popupbox)
        URcorners = find_subimage(screen, templates.popupButtonSelected.UR, popupbox)
        LLcorners = find_subimage(screen, templates.popupButtonSelected.LL, popupbox)
        LRcorners = find_subimage(screen, templates.popupButtonSelected.LR, popupbox)
    else:
        ULcorners = find_subimage(screen, templates.buttonSelected.UL)
        URcorners = find_subimage(screen, templates.buttonSelected.UR)
        LLcorners = find_subimage(screen, templates.buttonSelected.LL)
        LRcorners = find_subimage(screen, templates.buttonSelected.LR)
    quads = match_corners(ULcorners, URcorners, LLcorners, LRcorners)
    boxes = []
    for quad in quads:
        box = quad_to_box(quad)
        box = adjust_box(box)
        boxes.append(box)
    return boxes

def button_has_label(screen, button_box):
    magic_color = (13, 192, 255)
    label_box = box_to_label_finding_box(button_box)
    labelim = screen.crop(label_box)
    array = labelim.load()
    for x in xrange(labelim.size[0]):
        for y in xrange(labelim.size[1]):
            if array[x, y] == magic_color:
                return True
    return False

def OCR_title(screen_im_rgb, popup_box=None):
    screen_im_mono = screen_im_rgb.split()[2]
    title_box = get_title_box(popup_box)
    title_im_mono = screen_im_mono.crop(title_box)  # _orij #split
    title_im_bw = threshold_image(title_im_mono, 180)
    title_text = OCR_image(title_im_bw)
    return title_text

def OCR_button(screen_im_rgb, button_box):
    screen_im_mono = screen_im_rgb.split()[2]
    button_im_mono = screen_im_mono.crop(button_box)
    button_im_bw = threshold_image(button_im_mono, 100)
    button_text = OCR_image(button_im_bw)
    return button_text

def OCR_label(screen_im_rgb, label_box):
    screen_im_mono = screen_im_rgb.split()[2]
    label_im_mono = screen_im_mono.crop(label_box)
    label_im_bw = threshold_image(label_im_mono, 100)
    label_text = OCR_image(label_im_bw)
    return label_text

def OCR_help(screen_im_rgb):
    help_box = (20, 30, 780, 78)
    screen_im_mono = screen_im_rgb.split()[2]
    help_im_mono = screen_im_mono.crop(help_box)
    help_text = OCR_image(help_im_mono)
    return help_text

def convert_box_to_button(screen_im_rgb, button_box, popup_box=None):
    button_text = OCR_button(screen_im_rgb, button_box)
    coord = box_center(button_box)

    if button_has_label(screen_im_rgb, button_box):
        label_box = box_to_label_box(button_box)
        if popup_box != None:
            label_box = fit_box_inside_bounds(label_box, popup_box)
        label_text = OCR_label(screen_im_rgb, label_box)
        button_name = label_text
        button_value = button_text
        button = FieldButton(button_name, coord, button_value)
    else:
        button_name = button_text
        button = Button(button_name, coord)

    return button

class Parser(object):
    def __init__(self, session):
        self.session = session

    def click(self, button):
        coord = button.coord
        self.session.click(*coord)

    def press(self, hardbuttonname):
        try:
            self.session.press(HARD_BUTTONS[str(hardbuttonname).lower()])
        except KeyError, e:
            raise ValueError('Invalid hard button name: ' + str(e.value))

    def enter(self, screen, number):
        text = str(number)
        try:
            for char in text:
                self.click(screen.buttonmap[char])
        except KeyError, e:
            raise ValueError('Invalid numerical entry button name: ' + str(e.value))
        self.click(screen.buttonmap['OK'])

    def analyze(self, parent=None):
        # store screencap image
        screen_im_orij = self.session.screencap()
        screen_im_rgb = screen_im_orij.convert('RGB')

        # determine if popup or not, and store popup box if it is
        popup_box = get_popup_box(screen_im_rgb)
        is_popup = (popup_box != None)

        # find button boxes
        button_boxes = get_button_boxes(screen_im_rgb, popup_box)

        # create button object for each button box
        buttons = []
        names = []
        for button_box in button_boxes:
            button = convert_box_to_button(screen_im_rgb, button_box, popup_box)
            buttons.append(button)
            names.append(button.name)
        screenname = OCR_title(screen_im_rgb, popup_box)

        if '1' in names and '2' in names and '3' in names:
            screen = NumericalEntry(screenname, parent)
        else:
            if is_popup:
                screen = Screen(screenname, buttons, parent)
            else:
                screen = Screen(screenname, buttons)
        return screen

    def get_focus(self):
        # store screencap image
        screen_im_orij = self.session.screencap()
        screen_im_rgb = screen_im_orij.convert('RGB')

        # determine if popup or not, and store popup box if it is
        popup_box = get_popup_box(screen_im_rgb)
        is_popup = (popup_box != None)

        # find button box
        button_boxes = get_selected_button_boxes(screen_im_rgb, popup_box)
        if len(button_boxes) == 1:
            button_box = button_boxes[0]
            button = convert_box_to_button(screen_im_rgb, button_box, popup_box)
            return button
        else:
            return None

    def get_help_text(self):
        # store screencap image
        screen_im_orij = self.session.screencap()
        screen_im_rgb = screen_im_orij.convert('RGB')
        help_text = OCR_help(screen_im_rgb)
        return help_text

    def select_function(self, function):
        self.press('function')
        if function in SET_FUNCTION_MEASURE_MAP:
            self.session.click(*SET_FUNCTION_MEASURE_TAB)
            self.session.click(*(SET_FUNCTION_MEASURE_MAP[function]))
        if function in SET_FUNCTION_DIGITIZE_MAP:
            self.session.click(*SET_FUNCTION_DIGITIZE_TAB)
            self.session.click(*(SET_FUNCTION_DIGITIZE_MAP[function]))

    def menu_click(self, buttonname):
        self.session.click(*(MAIN_MENU_MAP[buttonname]))

    def __str__(self):
        return 'Parser on' + str(self.session)
