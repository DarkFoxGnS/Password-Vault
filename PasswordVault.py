import UserInterface as ui
from UserInterface import UIObject
def init():
    ui.init()
    
def update():

    userInput = ui.SCREEN.getch()
    print(userInput)

def shutdown():
    ui.shutdown()
    exit()

if __name__ == "__main__":
    SCREEN = init()
    
    objectArray = [UIObject(text="Option 1"),UIObject(y=1,text="Option 2")]
    ui.draw(objectArray)
    
    update()
    shutdown()
