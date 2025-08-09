import curses
import time
import PasswordVault

WIDTH = 0
HEIGHT = 0
SCREEN = None
WAIT_FOR_USER_INPUT = True
UI_SCENES = []

class SceneEnum():
    Main = 0
    Load = 1
    New = 2

ASCII_NUMBERS = [ord(x) for x in "0123456789"]

def computeScreenPosition(xOffset: "int or float",yOffset: "int or float"):
    if type(xOffset) == float:
        xOffset = int(xOffset * curses.COLS)
    if type(yOffset) == float:
        yOffset = int(yOffset * curses.ROWS)

    return xOffset,yOffset

class UIObject():
    def __init__(self,**kwargs: "x: int, y: int"):
       self.x = kwargs.get('x',0)
       self.y = kwargs.get('y',0)

    def draw(self, xOffset = 0, yOffset = 0):
        raise Exception(f"{self}.draw was not implemented!")

class UIRowSpacer(UIObject):
    def draw(self, xOffset = 0, yOffset = 0):
        pass

class UILabel(UIObject):
    def __init__(self,**kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        self.text = kwargs.get("text","Insert text here.")
    
    def draw(self, xOffset = 0, yOffset = 0):
        x,y = computeScreenPosition(self.x,self.y)
        SCREEN.addstr(y+yOffset,x+xOffset, self.text)

class UIInputObject(UIObject):
    def __init__(self, **kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        self.selected = False
        
    def input(self, keyCode: int):
        raise Exception(f"{self}.input was not implemented")

class UIButton(UIInputObject):
    def __init__(self, **kwargs: "x: int, y: int, text: str, function: function"):
        super().__init__(**kwargs)
        self.text = kwargs.get("text", "Button")
        self.function = kwargs.get("function",None)
    
    def input(self, keyCode: int):
        if (keyCode == 10):
            self.function()
            return True
        return False

    def draw(self, xOffset = 0, yOffset = 0):
        x,y = computeScreenPosition(self.x,self.y)
        SCREEN.addstr(y+yOffset,x+xOffset,self.text, [curses.A_BOLD,curses.A_REVERSE][self.selected])

class UITextInput(UIInputObject):
    def __init__(self,**kwargs: "x: int, y: int, text: str"):
        super().__init__(**kwargs)
        self.text = kwargs.get("text","")
        self.focused = False

    def input(self, keyCode: int):
        if not self.focused and not keyCode == 10:
            return False
        if keyCode == 10:
            self.focused = not self.focused
            return True
        if keyCode == 8:
            self.text = self.text[0:-1]
            return True
        if chr(keyCode).isprintable():
            self.text += chr(keyCode)
        return True

    def draw(self, xOffset = 0, yOffset = 0):
        x,y = computeScreenPosition(self.x,self.y)
        SCREEN.addstr(y+yOffset,x+xOffset, self.text[-50:]+"_"*(50-len(self.text)), [curses.A_UNDERLINE,curses.A_REVERSE][self.selected])
               

class UINumberInput(UITextInput):
    def input(self, keyCode: int):
        if not self.focused and not keyCode == 10:
            return False
        if keyCode == 10:
            self.focused = not self.focused
            return True
        if keyCode == 8:
            self.text = self.text[0:-1]
        if keyCode in ASCII_NUMBERS:
            self.text += chr(keyCode)
        return True

class UIContainer(UIObject):
    def __init__(self, **kwargs: "x: int, y: int, uiObjects: array"):
        super().__init__(**kwargs)
        self.uiObjects = []
        self.selectables = []
        self.selected = 0

        for uiObject in kwargs.get("uiObjects",[]):
            self.addObject(uiObject)

    def update(self):
        for yOffset in range(len(self.uiObjects)):
            self.uiObjects[yOffset].draw(yOffset = yOffset)
        
        userInput = SCREEN.getch()
        
        if not self.selectables[self.selected].input(userInput):
            match(userInput):
                case curses.KEY_UP:
                    self.selectables[self.selected].selected = False
                    self.selected -= 1
                    self.selected %= len(self.selectables)
                    self.selectables[self.selected].selected = True
                case curses.KEY_DOWN:
                    self.selectables[self.selected].selected = False
                    self.selected += 1
                    self.selected %= len(self.selectables)
                    self.selectables[self.selected].selected = True

    def addObject(self, uiObject: UIObject):
        if issubclass(type(uiObject),UIInputObject):
            if len(self.selectables) == 0:
                uiObject.selected = True
            self.selectables.append(uiObject)
        self.uiObjects.append(uiObject)

    def continues(self,data = None):
        pass
    
    def back(self):
        UI_SCENES.remove(self)
        UI_SCENES[-1].continues()
        SCREEN.clear()

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
    
    def loadFileFunction():
        initScene(SceneEnum.Load)

    def newFileFunction():
        initScene(SceneEnum.New)
    
    def exitFunction():
        PasswordVault.TUIShutdown()

    return UIContainer(uiObjects = [
        UILabel(text = "Password Vault"),
        UIRowSpacer(),
        UIButton(text = "Load file", function = loadFileFunction),
        UIButton(text = "New File", function = newFileFunction),
        UIButton(text = "Exit", function = exitFunction)
        ])

def drawLoadMenu():

    def backFunction():
        UI_SCENES[-1].back()
    
    return UIContainer(uiObjects = [
        UILabel(text = "Load password file"),
        UIRowSpacer(),
        UILabel(text = "File ID*"),
        UINumberInput(),
        UILabel(text = "Primary password*"),
        UITextInput(),
        UILabel(text = "Secondary password"),
        UITextInput(),
        UIRowSpacer(),
        UIButton(text = "Load", function = backFunction),
        UIButton(text = "Back", function = backFunction),
        UILabel(text = "* marked fields must be filled"),
        UILabel(text = "Whist a secondary password in not mandatory,"),
        UILabel(text = "it is recommended for added security."),
        ])

def initScene(sceneId: int):
    scene = None
    
    match(sceneId):
        case SceneEnum.Main:
            scene = drawMainMenu()
        case SceneEnum.Load:
            scene = drawLoadMenu()
        case SceneEnum.New:
            raise Exception("To be implemented")
            pass

    SCREEN.clear()
    UI_SCENES.append(scene)
