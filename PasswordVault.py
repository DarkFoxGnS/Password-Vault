import UserInterface as ui
import curses
import time

UI_CONTAINER = None
UI_SELECTABLES = []
SELECTED = 0

def init():
    ui.init()
    
    global UI_CONTAINER, UI_SELECTABLES
    UI_CONTAINER, UI_SELECTABLES = ui.drawMainMenu()
    UI_SELECTABLES[SELECTED].selected = True

    update()

def update():
    global SELECTED
    
    while True:
        UI_CONTAINER.draw()
        userInput = ui.SCREEN.getch()
        
        # if the user input was not consumed.
        if not UI_SELECTABLES[SELECTED].input(userInput):
            match(userInput):
                case curses.KEY_UP:
                    UI_SELECTABLES[SELECTED].selected = False
                    SELECTED -= 1
                    SELECTED %= len(UI_SELECTABLES)
                    UI_SELECTABLES[SELECTED].selected = True

                case curses.KEY_DOWN:
                    UI_SELECTABLES[SELECTED].selected = False
                    SELECTED += 1
                    SELECTED %= len(UI_SELECTABLES)
                    UI_SELECTABLES[SELECTED].selected = True
                case 113: # exit
                    exit()
                case curses.KEY_RESIZE:
                    curses.ROWS,curses.COLS = ui.SCREEN.getmaxyx()
                    ui.SCREEN.clear()

            if not ui.WAIT_FOR_USER_INPUT:
                time.sleep(0.016)

def shutdown():
    ui.shutdown()
    exit()

if __name__ == "__main__":
    SCREEN = init()
