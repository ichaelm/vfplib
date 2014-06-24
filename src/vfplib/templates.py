'''
Created on Jun 21, 2014

@author: Michael
'''

import os
from PIL import Image

this_dir, this_filename = os.path.split(__file__)
resources_dir = os.path.join(this_dir, 'resources')
templates_dir = os.path.join(resources_dir, 'templates')

def getImage(filename):
    return Image.open(os.path.join(templates_dir, filename)).convert('RGB')

class namedTuple(object):
    def __init__(self, UL, UR, LL, LR):
        self.UL = UL
        self.UR = UR
        self.LL = LL
        self.LR = LR

popup = namedTuple(
    getImage('ULcornerpopup.png'),
    getImage('URcornerpopup.png'),
    getImage('LLcornerpopup.png'),
    getImage('LRcornerpopup.png')
)
button = namedTuple(
    getImage('ULcorner.png'),
    getImage('URcorner.png'),
    getImage('LLcorner.png'),
    getImage('LRcorner.png')
)
buttonSelected = namedTuple(
    getImage('ULcornerselected.png'),
    getImage('URcornerselected.png'),
    getImage('LLcornerselected.png'),
    getImage('LRcornerselected.png')
)
popupButton = namedTuple(
    getImage('ULcornergrey.png'),
    getImage('URcornergrey.png'),
    getImage('LLcornergrey.png'),
    getImage('LRcornergrey.png')
)
popupButtonSelected = namedTuple(
    getImage('ULcornergreyselected.png'),
    getImage('URcornergreyselected.png'),
    getImage('LLcornergreyselected.png'),
    getImage('LRcornergreyselected.png')
)
