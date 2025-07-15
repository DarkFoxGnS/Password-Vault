import UserInterface as ui
import curses

UI_CONTAINER = None
UI_SELECTABLES = []
SELECTED = 0

def init():
    ui.init()
    
    global UI_CONTAINER, UI_SELECTABLES
    UI_CONTAINER, UI_SELECTABLES = ui.drawMainMenu()
    
    update()

def update():
    
    UI_CONTAINER.draw()
    userInput = ui.SCREEN.getch()
    
    if not UI_SELECTABLES[SELECTED].input(userInput):
        match(userInput):
            case curses.KEY_UP:
                print("up was pressed")
            case curses.KEY_DOWN:
                print("down was pressed")

def shutdown():
    ui.shutdown()
    exit()

if __name__ == "__main__":
    SCREEN = init()
