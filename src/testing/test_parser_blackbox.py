'''
Created on Jun 4, 2014

@author: mschaffe
'''

import unittest
from dummy_session import DummySession
from vfplib.parser import Parser
from vfplib.ui_structure import FieldButton

from PIL import Image
import os

class Test(unittest.TestCase):

    def setUp(self):
        self.session = DummySession()
        self.parser = Parser(self.session)
        this_dir, _ = os.path.split(__file__)
        resources_dir = os.path.join(this_dir, 'resources')
        screens_dir = os.path.join(resources_dir, 'screens')
        self.screenA = os.path.join(screens_dir, 'testA.png')
        self.screenB = os.path.join(screens_dir, 'testB.png')
        self.screenC = os.path.join(screens_dir, 'testC.png')
        self.screenD = os.path.join(screens_dir, 'testD.png')
        self.screenE = os.path.join(screens_dir, 'testE.png')
        self.screenF = os.path.join(screens_dir, 'testF.png')

    def tearDown(self):
        pass

    def testA(self):
        expectedscreenname = 'Measurement Window'
        expectedbuttonmap = {'Units':'NPLCs', 'NPLCs':'1plc', 'Cancel':None, 'OK':None}
        self.session.set_screen(Image.open(self.screenA))
        screen = self.parser.analyze(None)
        self.assertEqual(self.session.log, ['screencap()'])
        # TODO: assert has parent
        self.assertEqual(screen.title, expectedscreenname)
        self.assertEqual(len(screen.buttonmap), len(expectedbuttonmap))
        for button in screen.buttonmap.values():
            self.assertIn(button.name, expectedbuttonmap)
            if expectedbuttonmap[button.name] == None:
                self.assertNotIsInstance(button, FieldButton)
            else:
                self.assertIsInstance(button, FieldButton)
                self.assertEqual(button.setting, expectedbuttonmap[button.name])
            del expectedbuttonmap[button.name]

    def testB(self):
        expectedscreenname = 'Auto Delay'
        expectedbuttonmap = {'Off':None, 'On':None, 'Cancel':None}
        self.session.set_screen(Image.open(self.screenB))
        screen = self.parser.analyze(None)
        self.assertEqual(self.session.log, ['screencap()'])
        # TODO: assert has parent
        self.assertEqual(screen.title, expectedscreenname)
        self.assertEqual(len(screen.buttonmap), len(expectedbuttonmap))
        for button in screen.buttonmap.values():
            self.assertIn(button.name, expectedbuttonmap)
            if expectedbuttonmap[button.name] == None:
                self.assertNotIsInstance(button, FieldButton)
            else:
                self.assertIsInstance(button, FieldButton)
                self.assertEqual(button.setting, expectedbuttonmap[button.name])
            del expectedbuttonmap[button.name]

    def testC(self):
        # expectedscreenname = 'UNIMPLEMENTED FOR TABS'
        expectedbuttonmap = {'Trigger Type':'Manual', 'Trigger Position':'50%', 'Trigger Delay':'0.00s'}
        self.session.set_screen(Image.open(self.screenC))
        screen = self.parser.analyze(None)
        self.assertEqual(self.session.log, ['screencap()'])
        # TODO: assert has no parent
        # self.assertEqual(screen.title, expectedscreenname)
        self.assertEqual(len(screen.buttonmap), len(expectedbuttonmap))
        for button in screen.buttonmap.values():
            self.assertIn(button.name, expectedbuttonmap)
            if expectedbuttonmap[button.name] == None:
                self.assertNotIsInstance(button, FieldButton)
            else:
                self.assertIsInstance(button, FieldButton)
                self.assertEqual(button.setting, expectedbuttonmap[button.name])
            del expectedbuttonmap[button.name]

    def testD(self):
        expectedscreenname = 'Trigger Source'
        expectedbuttonmap = {'Dig I/O':None, 'TSP Link':None, 'BNC':None, 'Cancel':None}
        self.session.set_screen(Image.open(self.screenD))
        screen = self.parser.analyze(None)
        self.assertEqual(self.session.log, ['screencap()'])
        # TODO: assert has parent
        self.assertEqual(screen.title, expectedscreenname)
        self.assertEqual(len(screen.buttonmap), len(expectedbuttonmap))
        for button in screen.buttonmap.values():
            self.assertIn(button.name, expectedbuttonmap)
            if expectedbuttonmap[button.name] == None:
                self.assertNotIsInstance(button, FieldButton)
            else:
                self.assertIsInstance(button, FieldButton)
                self.assertEqual(button.setting, expectedbuttonmap[button.name])
            del expectedbuttonmap[button.name]

    def testE(self):
        expectedscreenname = 'Auto Y-Scale Type'
        expectedbuttonmap = {'Off':None, 'Per Trace':None, 'Swim Lane':None, 'Common':None, 'Cancel':None}
        self.session.set_screen(Image.open(self.screenE))
        screen = self.parser.analyze(None)
        self.assertEqual(self.session.log, ['screencap()'])
        # TODO: assert has parent
        self.assertEqual(screen.title, expectedscreenname)
        self.assertEqual(len(screen.buttonmap), len(expectedbuttonmap))
        for button in screen.buttonmap.values():
            self.assertIn(button.name, expectedbuttonmap)
            if expectedbuttonmap[button.name] == None:
                self.assertNotIsInstance(button, FieldButton)
            else:
                self.assertIsInstance(button, FieldButton)
                self.assertEqual(button.setting, expectedbuttonmap[button.name])
            del expectedbuttonmap[button.name]

    def testF(self):
        expectedscreenname = 'Measurement Aperture'
        expectedbuttonmap = {
            '1'      : None,
            '2'      : None,
            '3'      : None,
            '4'      : None,
            '5'      : None,
            '6'      : None,
            '7'      : None,
            '8'      : None,
            '9'      : None,
            '0'      : None,
            '+/-'    : None,
            '.'      : None,
            'Clear'  : None,
            'OK'     : None,
            'Cancel' : None
        }
        self.session.set_screen(Image.open(self.screenF))
        screen = self.parser.analyze(None)
        self.assertEqual(self.session.log, ['screencap()'])
        # TODO: assert has parent
        self.assertEqual(screen.title, expectedscreenname)
        self.assertEqual(len(screen.buttonmap), len(expectedbuttonmap))
        for button in screen.buttonmap.values():
            self.assertIn(button.name, expectedbuttonmap)
            if expectedbuttonmap[button.name] == None:
                self.assertNotIsInstance(button, FieldButton)
            else:
                self.assertIsInstance(button, FieldButton)
                self.assertEqual(button.setting, expectedbuttonmap[button.name])
            del expectedbuttonmap[button.name]
        self.parser.enter(screen, '8675309')
        self.assertEqual(self.session.log, [
            'screencap()',
            'click(311, 175)',
            'click(394, 258)',
            'click(228, 175)',
            'click(311, 258)',
            'click(394, 341)',
            'click(228, 424)',
            'click(394, 175)',
            'click(669, 341)',  # OK button
        ])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
