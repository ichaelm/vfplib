'''
Created on Jun 10, 2014

@author: mschaffe
'''

from vfplib.parser import Screen, Button, Parser

dummyscreenmap = {'root' : Screen('root', [Button('root_to_A_if_x=1;B', (0, 0)),
                                           Button('root_to_C', (0, 0)), ]),
                  'A'    : Screen('A', [Button('A_to_root_set_x=0', (0, 0)),
                                        Button('A_to_root_set_x=1', (0, 0)),
                                        Button('A_to_C', (0, 0)), ]),
                  'B'    : Screen('B', [Button('B_to_root_set_x=0', (0, 0)),
                                        Button('B_to_root_set_x=1', (0, 0)),
                                        Button('B_to_C', (0, 0)), ]),
                  'C'    : Screen('C', [Button('C_to_root', (0, 0)),
                                        Button('C_to_C', (0, 0)),
                                        Button('C_to_D', (0, 0)), ]),
                  'D'    : Screen('D', [Button('D_to_root', (0, 0)), ]),
                  }

defaultstate = {'x' : '0'}

class DummyParser(Parser):
    def __init__(self):
        self.currentscreen = dummyscreenmap['root']
        self.numscreencaps = 0
        self.state = defaultstate
    def click(self, button):
        assert isinstance(button, Button)
        sourcename = button.name.partition('_to_')[0]
        targetname = button.name.partition('_set_')[0].partition('_to_')[2]
        setting = button.name.partition('_set_')[2]
        if setting != '':
            var = setting.partition('=')[0]
            value = setting.partition('=')[2]
            self.state[var] = value
        if 'if' in targetname:
            first = targetname.partition(';')[0]
            second = targetname.partition(';')[2]
            truetarget = first.partition('_if_')[0]
            condition = first.partition('_if_')[2]
            falsetarget = second
            conditionvar = condition.partition('=')[0]
            conditionvalue = condition.partition('=')[2]
            if (self.state[conditionvar] == conditionvalue):
                targetname = truetarget
            else:
                targetname = falsetarget
        assert sourcename == self.currentscreen.title
        assert targetname in dummyscreenmap.keys()
        self.currentscreen = dummyscreenmap[targetname]
    def press(self, hardbuttonname):
        raise NotImplementedError()
    def enter(self, number):
        raise NotImplementedError()
    def analyze(self, _):
        self.numscreencaps = self.numscreencaps + 1
        return self.currentscreen
