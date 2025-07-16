import curses
import time
from enum import Enum
import PasswordVault

WIDTH = 0
HEIGHT = 0
SCREEN = None
WAIT_FOR_USER_INPUT = True

ASCII_LETTERS = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90] 

def computeScreenPosition(xOffset: "int or float",yOffset: "int or float"):
    if type(xOffset) == float:
        xOffset = int(xOffset * curses.COLS)
    if type(yOffset) == float:
        yOffset = int(yOffset * curses.ROWS)

    return xOffset,yOffset

class UI_Object():
    def __init__(self,**kwargs: "x: int, y: int"):
       self.x = kwargs.get('x',0)
       self.y = kwargs.get('y',0)

    def draw(self, xOffset = 0, yOffset = 0):
        raise Exception(f"{self}.draw was not implemented!")

class UI_RowSpacer(UI_Object):
    def draw(self, xOffset = 0, yOffset = 0):
        pass

class UI_Label(UI_Object):
    def __init__(self,**kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        self.text = kwargs.get("text","Insert text here.")
    
    def draw(self, xOffset = 0, yOffset = 0):
        x,y = computeScreenPosition(self.x,self.y)
        SCREEN.addstr(y+yOffset,x+xOffset, self.text)

class UI_InputObject(UI_Object):
    def __init__(self, **kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        self.selected = False
        
    def input(self, keyCode: int):
        raise Exception(f"{self}.input was not implemented")

class UI_Button(UI_InputObject):
    def __init__(self, **kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        self.text = kwargs.get("text", "Button")
        self.function = None
    
    def input(self, keyCode: int):
        if (keyCode == 10):
            self.function()
            return True
        return False

    def draw(self, xOffset = 0, yOffset = 0):
        x,y = computeScreenPosition(self.x,self.y)
        SCREEN.addstr(y+yOffset,x+xOffset,self.text, [curses.A_NORMAL,curses.A_REVERSE][self.selected])

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

def switchInputBlocking():
    global WAIT_FOR_USER_INPUT
    WAIT_FOR_USER_INPUT = not WAIT_FOR_USER_INPUT
    SCREEN.nodelay( not WAIT_FOR_USER_INPUT)

def shutdown():
    """
    Safely shutdowns curses and exits the program.
    """
    SCREEN.keypad(0)
    SCREEN.nodelay(False)
    curses.nocbreak()
    curses.echo()
    curses.curs_set(True)
    curses.endwin()

def init():
    """
    Initiates curses and starts the basic drawing.
    """
    global WIDTH, HEIGHT, SCREEN
    SCREEN = curses.initscr()
    
    curses.curs_set(False)
    curses.cbreak()
    curses.noecho()
    SCREEN.keypad(1)
    HEIGHT, WIDTH = SCREEN.getmaxyx()

    return SCREEN

#########################################################
# UI constuctor functions
def drawMainMenu():
    selectables = []
    container = UI_Container()
    
    tempObject = UI_Label(text = "Password Vault", x = 0.45)
    container.addObject(tempObject)
    
    tempObject = UI_RowSpacer(x = 0.45)
    container.addObject(tempObject)

    tempObject = UI_Button(x = 0.45, text = "Load file")
    tempObject.function = lambda:(
        print("File was loaded.")
        )
    selectables.append(tempObject)
    container.addObject(tempObject)

    tempObject = UI_Button(x = 0.45, text = "New File")
    tempObject.function = lambda:(
        print("A new file was created.")
        )
    selectables.append(tempObject)
    container.addObject(tempObject)
    
    tempObject = UI_Button(x = 0.45, text = "Exit")
    tempObject.function = lambda:(
        PasswordVault.shutdown()
    )
    selectables.append(tempObject)
    container.addObject(tempObject)

    return container,selectables
