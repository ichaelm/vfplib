'''
Created on Aug 6, 2014

@author: mschaffe
'''
import unittest
from vfplib.ui_structure import Button, FieldButton, Screen
import vfplib.crawler as crawler

class Test(unittest.TestCase):
    def testMergeButtons(self):
        a = Button('a', (0, 0))
        b_1 = FieldButton('b', (0, 1), 'b_1')
        b_2 = FieldButton('b', (0, 1), 'b_2')
        diff1 = crawler.merge_buttons(b_1, b_2)
        self.assertEquals(b_2.setting, 'b_1')
        self.assertEquals(b_2.settings, set(['b_1', 'b_2']))
        diff2 = crawler.merge_buttons(b_2, b_1)
        self.assertEquals(diff1, set(['b_1']))
        self.assertEquals(diff2, set(['b_2']))
        self.assertEquals(b_1.setting, 'b_1')
        self.assertEquals(b_1.settings, set(['b_1', 'b_2']))
        # TODO: add more corner case coverage

    def testMergeScreens(self):
        ba = Button('ba', (0, 0))
        bb_1 = FieldButton('bb', (0, 1), 'bb_1')
        bb_2 = FieldButton('bb', (0, 1), 'bb_2')
        bb_3 = FieldButton('bb', (0, 1), 'bb_3')
        bc_1 = FieldButton('bc', (0, 2), 'bc_1')
        bc_2 = FieldButton('bc', (0, 2), 'bc_2')
        bd_1 = FieldButton('bd', (0, 3), 'bd_1')
        a = Screen('a', [ba, bb_1, bc_1, bd_1])
        b = Screen('a', [ba, bb_2, bc_2, bd_1])
        c = Screen('a', [ba, bb_3, bc_1, bd_1])
        diffs1 = crawler.merge_screens(c, b)
        diffs2 = crawler.merge_screens(b, a)
        self.assertEquals(diffs1, {'ba': set(), 'bb': set(['bb_3']), 'bc': set(['bc_1']), 'bd': set()})
        self.assertEquals(diffs2, {'ba': set(), 'bb': set(['bb_2', 'bb_3']), 'bc': set(['bc_2']), 'bd': set()})
        self.assertEquals(b.buttonmap['bb'].setting, 'bb_3')
        self.assertEquals(b.buttonmap['bb'].settings, set(['bb_2', 'bb_3']))
        self.assertEquals(b.buttonmap['bc'].setting, 'bc_1')
        self.assertEquals(b.buttonmap['bc'].settings, set(['bc_1', 'bc_2']))
        self.assertEquals(b.buttonmap['bd'].setting, 'bd_1')
        self.assertEquals(b.buttonmap['bd'].settings, set(['bd_1']))
        self.assertEquals(a.buttonmap['bb'].setting, 'bb_3')
        self.assertEquals(a.buttonmap['bb'].settings, set(['bb_1', 'bb_2', 'bb_3']))
        self.assertEquals(a.buttonmap['bc'].setting, 'bc_1')
        self.assertEquals(a.buttonmap['bc'].settings, set(['bc_1', 'bc_2']))
        self.assertEquals(a.buttonmap['bd'].setting, 'bd_1')
        self.assertEquals(a.buttonmap['bd'].settings, set(['bd_1']))
        # TODO: add more corner case coverage


if __name__ == "__main__":
    unittest.main()
