import curses
import time
from enum import Enum

WIDTH = 0
HEIGHT = 0
SCREEN = None
WAIT_FOR_USER_INPUT = False

class UIObject():
    def __init__(self,**kwargs: "x: int,y:int ,text: str"):
       self.x = kwargs.get('x',0)
       self.y = kwargs.get('y',0)
       self.text = kwargs.get('text',"")
       self.selected = kwargs.get('selected',False)

    def draw(self, screen: curses.window):
        screen.addstr(self.y,self.x,self.text,[0,curses.A_STANDOUT][self.selected])

##########################################################
# UI related functions.
def shutdown():
    """
    Safely shutdowns curses and exits the program.
    """
    SCREEN.keypad(0)
    SCREEN.nodelay(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def init():
    """
    Initiates curses and starts the basic drawing.
    """
    global WIDTH, HEIGHT, SCREEN
    SCREEN = curses.initscr()

    curses.cbreak()
    curses.noecho()
    SCREEN.keypad(1)
    HEIGHT, WIDTH = SCREEN.getmaxyx()

    return SCREEN

def update(uiObject: UIObject):
    uiObject.draw(SCREEN)

def draw(UIObjects: list):
    for uiObj in UIObjects:
        print(uiObj)
        uiObj.draw(SCREEN)
    SCREEN.refresh()

