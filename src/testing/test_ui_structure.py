'''
Created on Jun 25, 2014

@author: mschaffe
'''
import unittest

from vfplib.ui_structure import Button, FieldButton, Screen, NumericalEntry

class Test(unittest.TestCase):

    def assertEqualityContract(self, a, b, expected, message=None):
        if message == None:
            message = str(a) + ' and ' + str(b)
        self.assertEqual(a == b, expected, 'Equality contract broken for: ' + message)
        self.assertEqual(b == a, expected, 'Equality contract broken for: ' + message)
        self.assertEqual(a != b, not expected, 'Equality contract broken for: ' + message)
        self.assertEqual(b != a, not expected, 'Equality contract broken for: ' + message)

    def assertHashContract(self, a, b, message=None):
        if message == None:
            message = str(a) + ' and ' + str(b)
        if a == b:
            self.assertEqual(hash(a), hash(b), 'Hash contract broken for: ' + message)
        else:
            self.assertNotEqual(hash(a), hash(b), 'Hash contract quasi-broken for: ' + message)

    def testButtonInit(self):
        a = Button('test name A', (11, 22))
        self.assertEquals(a.name, 'test name A', 'Button.__init__: Problem setting Button.name')
        self.assertEquals(a.coord, (11, 22), 'Button.__init__: Problem setting Button.coord')

    def testButtonEquality(self):
        a = Button('test name A', (11, 22))
        b = Button('test name B', (11, 22))
        c = Button('test name A', (22, 11))
        a2 = Button('test name A', (11, 22))
        other = 'Button: test name A'
        class DummySubButton(Button):
            pass
        asub = DummySubButton('test name C', (11, 22))
        self.assertEqualityContract(a, a, True, 'same Button object')
        self.assertEqualityContract(a, b, False, 'different Button.name')
        self.assertEqualityContract(a, c, False, 'different Button.coord')
        self.assertEqualityContract(a, a2, True, 'identical Button objects')
        self.assertEqualityContract(a, other, False, 'non-Button objects')
        self.assertEqualityContract(a, asub, False, 'subclasses')

    def testButtonHash(self):
        try:
            _ = hash(Button({}, (0, 0)))
            self.assertTrue(False, 'Button.__hash__: Failed to throw TypeError exception on unhashable Button.name')
        except TypeError, e:
            if str(e) != "unhashable type: 'dict'":
                raise
        try:
            _ = hash(Button('', (set(), 0)))
            self.assertTrue(False, 'Button.__hash__: Failed to throw TypeError exception on unhashable Button.coord')
        except TypeError, e:
            if str(e) != "unhashable type: 'set'":
                raise
        a = Button('test name A', (11, 22))
        b = Button('test name B', (11, 22))
        c = Button('test name A', (22, 11))
        a2 = Button('test name A', (11, 22))
        other = 'Button: test name A'
        class DummySubButton(Button):
            pass
        asub = DummySubButton('test name C', (11, 22))
        self.assertHashContract(a, a, 'same Button object')
        self.assertHashContract(a, b, 'different Button.name')
        self.assertHashContract(a, c, 'different Button.coord')
        self.assertHashContract(a, a2, 'identical Button objects')
        self.assertHashContract(a, other, 'non-Button objects')
        self.assertHashContract(a, asub, 'subclasses')

    def testButtonStr(self):
        a = Button('test name A', (11, 22))
        self.assertEquals(str(a), 'Button: test name A', 'Button.__str__ is incorrect')

    def testFieldButtonInit(self):
        a = FieldButton('test name A', (11, 22), 'setting A')
        # b = FieldButton('test name A', (11, 22)) #unimplemented
        self.assertEquals(a.name, 'test name A', 'FieldButton.__init__: Problem setting FieldButton.name')
        self.assertEquals(a.coord, (11, 22), 'FieldButton.__init__: Problem setting FieldButton.coord')
        self.assertEquals(a.setting, 'setting A', 'FieldButton.__init__: Problem setting FieldButton.setting')
        # self.assertEquals(b.setting, None, 'FieldButton.__init__: Problem with FieldButton.setting default value')  # unimplemented

    def testFieldButtonStr(self):
        a = FieldButton('test name A', (11, 22), 'setting A')
        self.assertEquals(str(a), 'FieldButton: test name A', 'FieldButton.__str__ is incorrect')

    def testScreenInit(self):
        ba = Button('test button A', (1, 2))
        bb = Button('test button B', (3, 4))
        bc = Button('test button C', (5, 6))
        a = Screen('test screen A', [])
        b = Screen('test screen B', [ba])
        c = Screen('test screen C', [ba, bb, bc])
        d = Screen('test screen C', [bc, bb, ba], a)
        # exceptions
        try:
            _ = Screen('invalid buttons', 1)
            self.assertTrue(False, 'Screen.__init__: Failed to throw TypeError exception on non-iterable buttons')
        except TypeError, e:
            if str(e) != "'int' object is not iterable":
                raise
        try:
            _ = Screen('invalid buttons', 'string')
            self.assertTrue(False, 'Screen.__init__: Failed to throw TypeError exception on buttons without .name')
        except AttributeError, e:
            if str(e) != "'str' object has no attribute 'name'":
                raise
        # title parameter
        self.assertEquals(a.title, 'test screen A', 'Screen.__init__: Problem setting Screen.title')
        # buttonmap parameter
        self.assertEquals(a.buttonmap, {}, 'Screen.__init__: Problem initializing screen with 0 buttons')
        self.assertEquals(b.buttonmap, {'test button A': ba}, 'Screen.__init__: Problem initializing screen with 1 button')
        self.assertEquals(c.buttonmap, {
            'test button A': ba,
            'test button B': bb,
            'test button C': bc
        }, 'Screen.__init__: Problem initializing screen with multiple buttons')
        self.assertEquals(d.buttonmap, c.buttonmap, 'Screen.__init__: Problem with ordering of buttons')
        # parent parameter
        self.assertEquals(a.parent, None, 'Screen.__init__: Problem with default value of Screen.parent')
        self.assertEquals(d.parent, a, 'Screen.__init__: Problem setting Screen.parent')

    def testScreenEquality(self):
        ba = Button('test button A', (1, 2))
        bb = Button('test button B', (3, 4))
        bc = Button('test button C', (5, 6))
        bc2 = Button('test button C', (7, 8))
        bc3 = Button('test button D', (5, 6))
        a = Screen('test screen A', [])
        b = Screen('test screen B', [ba])
        d = Screen('test screen C', [bc, bb, ba], a)
        d2 = Screen('test screen C', [ba, bb, bc], a)
        class DummySubScreen(Screen):
            pass
        dsub = DummySubScreen('test screen C', [ba, bb, bc], a)
        e = Screen('test screen D', [bc, bb, ba], a)
        f = Screen('test screen C', [bc, bb], a)
        g = Screen('test screen C', [bc, bb, ba], b)
        h = Screen('test screen C', [bc2, bb, ba], a)
        i = Screen('test screen C', [bc3, bb, ba], a)
        self.assertEqualityContract(d, d, True, 'same Screen object')
        self.assertEqualityContract(d, e, False, 'different Screen.title')
        self.assertEqualityContract(d, f, False, 'different Screen.buttonmap')
        self.assertEqualityContract(d, g, False, 'different Screen.parent')
        self.assertEqualityContract(d, h, False, 'one button has same name but different coord')
        self.assertEqualityContract(d, i, False, 'one button has same coord but different name')
        self.assertEqualityContract(d, d2, True, 'identical Screen objects')
        self.assertEqualityContract(d, dsub, True, 'subclasses')

    def testScreenHash(self):
        try:
            _ = hash(Screen({}, [Button('', (0, 0))]))
            self.assertTrue(False, 'Screen.__hash__: Failed to throw TypeError exception on unhashable Screen.title')
        except TypeError, e:
            if str(e) != "unhashable type: 'dict'":
                raise
        class Dummy(object):
            name = {}
        try:
            _ = hash(Screen('', [Dummy()]))
            self.assertTrue(False, 'Screen.__hash__: Failed to throw TypeError on unhashable keys in Screen.buttonmap')
        except TypeError, e:
            if str(e) != "unhashable type: 'dict'":
                raise
        class Dummy2(object):
            __hash__ = None
            name = 'dummy name'
        try:
            _ = hash(Screen('', [Dummy2()]))
            self.assertTrue(False, 'Screen.__hash__: Failed to throw TypeError on unhashable values in Screen.buttonmap')
        except TypeError, e:
            if str(e) != "unhashable type: 'Dummy2'":
                raise
        try:
            _ = hash(Screen('', [Button('', (0, 0))], []))
            self.assertTrue(False, 'Screen.__hash__: Failed to throw TypeError on unhashable Screen.parent')
        except TypeError, e:
            if str(e) != "unhashable type: 'list'":
                raise
        try:
            _ = hash(Screen('', [Button('', (0, 0))], 7.1))
        except TypeError:
            raise
        ba = Button('test button A', (1, 2))
        bb = Button('test button B', (3, 4))
        bc = Button('test button C', (5, 6))
        bc2 = Button('test button C', (7, 8))
        bc3 = Button('test button D', (5, 6))
        a = Screen('test screen A', [])
        b = Screen('test screen B', [ba])
        d = Screen('test screen C', [bc, bb, ba], a)
        d2 = Screen('test screen C', [ba, bb, bc], a)
        class DummySubScreen(Screen):
            pass
        dsub = DummySubScreen('test screen C', [ba, bb, bc], a)
        e = Screen('test screen D', [bc, bb, ba], a)
        f = Screen('test screen C', [bc, bb], a)
        g = Screen('test screen C', [bc, bb, ba], b)
        h = Screen('test screen C', [bc2, bb, ba], a)
        i = Screen('test screen C', [bc3, bb, ba], a)
        self.assertHashContract(d, d, 'same Screen object')
        self.assertHashContract(d, e, 'different Screen.title')
        self.assertHashContract(d, f, 'different Screen.buttonmap')
        self.assertHashContract(d, g, 'different Screen.parent')
        self.assertHashContract(d, h, 'one button has same name but different coord')
        self.assertHashContract(d, i, 'one button has same coord but different name')
        self.assertHashContract(d, d2, 'identical screen objects')
        self.assertHashContract(d, dsub, 'subclasses')

    def testScreenStr(self):
        a = Screen('test screen A', [])
        d = Screen('test screen C', [], a)
        self.assertEquals(str(a), 'Screen: test screen A', 'Screen.__str__ incorrectly handles parentless Screen')
        self.assertEquals(str(d), 'Screen: test screen C (child of Screen: test screen A)', 'Screen.__str__ incorrectly handles Screen with parent')

    def testNumericalEntryInit(self):
        a = NumericalEntry('test title A')
        b = NumericalEntry('test title A', a)
        self.assertEquals(a.title, 'test title A', 'NumericalEntry.__init__: Problem setting NumericalEntry.title')
        self.assertEquals(set(a.buttonmap.values()), set(NumericalEntry.NUMERICAL_ENTRY_BUTTONS), 'NumericalEntry.__init__: Problem setting NumericalEntry.buttonmap')
        self.assertEquals(a.parent, None, 'NumericalEntry.__init__: Problem with NumericalEntry.parent default value')
        self.assertEquals(b.parent, a, 'NumericalEntry.__init__: Problem setting NumericalEntry.parent')

    def testNumericalEntryStr(self):
        a = NumericalEntry('test title A')
        b = NumericalEntry('test title B', a)  # unimplemented
        self.assertEquals(str(a), 'NumericalEntry: test title A', 'NumericalEntry.__str__ incorrectly handles parentless NumericalEntry')
        # self.assertEquals(str(b), 'NumericalEntry: test title B (child of NumericalEntry: test title A)', 'NumericalEntry.__str__ incorrectly handles NumericalEntry with parent') # unimplemented

if __name__ == "__main__":
    unittest.main()
