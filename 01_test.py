from time import sleep
from asciimatics.screen import ManagedScreen, Screen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.event import KeyboardEvent

import time
from collections import namedtuple 
      
# Declaring namedtuple()  
TypedChar = namedtuple('TypedChar',['char','timestamp'])

class TypingText:
    """
    A class to keep track of what is to be typed and what was 
    """

    def __init__(self, targettext):
        self.targettext = list(targettext)
        self.typedtext = list()
        self.starttime = -1

    def processKeystroke(self, key):
        '''
        Key bindings are available here: https://github.com/peterbrittain/asciimatics/blob/master/asciimatics/screen.py
        '''
        if key == Screen.KEY_BACK:
            if len(self.typedtext) > 0:
                self.typedtext.pop()
        else:
            if len(self.typedtext) == 0:
                self.starttime = time.time()
            if ord('A') <= key <= ord('Z') or ord('a') <= key <= ord('z') or key == ord(' '):
                self.typedtext.append(TypedChar(chr(key), time.time()))

    def getWordsPerMin(self):
        errors = 0
        for i, val in enumerate(self.typedtext):
            if val.char != self.targettext[i]:
                errors += 1

        if len(self.typedtext) == len(self.targettext):
            return 60*(len(self.typedtext) - errors)/(5*(self.typedtext[-1].timestamp - self.starttime))
        else:
            return 60*(len(self.typedtext) - errors)/(5*(time.time() - self.starttime))

    def printText(self, screen):


        # COLOUR_BLACK = 0
        # COLOUR_RED = 1
        # COLOUR_GREEN = 2
        # COLOUR_YELLOW = 3
        # COLOUR_BLUE = 4
        # COLOUR_MAGENTA = 5
        # COLOUR_CYAN = 6
        # COLOUR_WHITE = 7

        startx = 10
        starty = 10

        if len(self.typedtext)> 2:
            # screen.paint("{0:.1f} WPM          ".format(self.getWordsPerMin()), startx, starty-3)
            screen.paint(f"{self.getWordsPerMin():10.2f} WPM", startx, starty-3)

        for offset, ch in enumerate(self.targettext):
            if offset >= len(self.typedtext):
                screen.paint(
                    ch, 
                    startx+offset, 
                    starty,
                    colour=4
                )        
            elif self.typedtext[offset].char == ch:
                screen.paint(
                    ch, 
                    startx+offset, 
                    starty,
                    colour=2
                )
            else:
                screen.paint(
                    ch, 
                    startx+offset, 
                    starty,
                    colour=1
                )

def demo():
    t = TypingText('Lost time is never found again')
    with ManagedScreen() as screen:
        while True:
            event = screen.get_event()
            if isinstance(event, KeyboardEvent):
                if event.key_code == Screen.KEY_F1:
                    break
                t.processKeystroke(event.key_code)
            t.printText(screen)
            screen.refresh()


demo()