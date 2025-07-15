import curses
import time
from enum import Enum

WIDTH = 0
HEIGHT = 0
SCREEN = None
WAIT_FOR_USER_INPUT = False

ASCII_LETTERS = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90] 

class UI_Object():
    def __init__(self,**kwargs: "x: int, y: int"):
       self.x = kwargs.get('x',0)
       self.y = kwargs.get('y',0)

    def draw(self, xOffset = 0, yOffset = 0):
        raise Exception(f"{self}.draw was not implemented!")

class UI_Label(UI_Object):
    def __init__(self,**kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        self.text = kwargs.get("text","Insert text here.")
    
    def draw(self, xOffset = 0, yOffset = 0):
        SCREEN.addstr(self.y+yOffset,self.x+xOffset, "label")

class UI_InputObject(UI_Object):

    def __init__(self, **kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        
    def input(self, keyCode: int):
        return False

class UI_Button(UI_InputObject):
    def __init__(self, **kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        self.text = kwargs.get("text", "Button")
        self.selected = False
    
    def input(self, keyCode: int):
        if (keyCode == 10):
            print("Enter was pressed")
        return False

    def draw(self, xOffset = 0, yOffset = 0):
        SCREEN.addstr(self.y+yOffset,self.x+xOffset,self.text, [curses.A_NORMAL,curses.A_REVERSE][self.selected])

class UI_Container(UI_Object):
    def __init__(self, **kwargs: "x: int, y: int"):
        super().__init__(**kwargs)
        self.uiObjects = []

    def draw(self):
        for yOffset in range(len(self.uiObjects)):
            self.uiObjects[yOffset].draw(yOffset = yOffset)

    def addObject(self, uiObject: UI_Object):
        self.uiObjects.append(uiObject)

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

def drawMainMenu():
    selectables = []
    container = UI_Container()
    
    tempObject = UI_Button()
    
    selectables.append(tempObject)
    container.addObject(tempObject)

    tempObject = UI_Label(text = "Hello World")
    container.addObject(tempObject)

    tempObject = UI_Button()
    selectables.append(tempObject)
    container.addObject(tempObject)

    return container,selectables
