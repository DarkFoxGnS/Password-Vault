import curses
import time
import sys


def TUIInit():
    import TerminalUserInterface as tui
    tui.init()
    tui.initScene(0)
    TUIUpdate()

def TUIUpdate():
    import TerminalUserInterface as tui
    while True:
        frameStart = time.time()

        tui.UI_SCENES[-1].update()
        
        if not tui.WAIT_FOR_USER_INPUT:
            time.sleep(0.016-(frameStart-time.time()))

def TUIShutdown():
    import TerminalUserInterface as tui
    tui.shutdown()
    exit()

def parseArgs():
    for i in range(1,len(sys.argv)):
        arg = sys.argv[i]
        if arg.startswith("-h"):
            #Headless start
            pass
        if arg.startswith("-t"):
            #TUI start
            TUIInit()
        if arg.startswith("-q"):
            #QT start
            pass
            

if __name__ == "__main__":
    parseArgs()
