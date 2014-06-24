'''
Created on Jun 4, 2014

@author: mschaffe
'''

from PIL import Image

from vfplib.session import Session

class DummySession(Session):
    def __init__(self, imagepath=None):
        if imagepath != None:
            self.currentscreen = Image.open(imagepath)
        self.log = []
    def screencap(self):
        self.log.append('screencap()')
        return self.currentscreen
    def click(self, x, y):
        self.log.append('click(' + str(x) + ', ' + str(y) + ')')
    def drag(self, x1, y1, x2, y2):
        self.log.append('drag(' + str(x1) + ', ' + str(y1) + ', ' + str(x2) + ', ' + str(y2) + ')')
    def press(self, buttonnumber):
        self.log.append('press(' + str(buttonnumber) + ')')
    def get_log(self):
        return self.log
    def set_screen(self, image):
        self.currentscreen = image
