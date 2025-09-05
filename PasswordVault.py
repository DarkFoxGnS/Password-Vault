import curses
import time
import sys
import KeyFile

class launchStateEnum():
    Headless = 0
    CLI = 1
    TUI = 2
    GUI = 3

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

def CLIInit():
    import CLIUserInterface as cui
    cui.init()
    CLIUpdate()

def CLIUpdate():
    import CLIUserInterface as cui
    cui.update()


def parseArgs():
    args = {
            "launchState":launchStateEnum.TUI,
            "cmd":[],
            }
    for i in range(1,len(sys.argv)):
        from KeyFile import KeyFile
        arg = sys.argv[i]
        keyFile = KeyFile.getKeyFile()

        if arg == "-h":
            print("TODO: Print Help over here")
            exit()

        if arg == "-headless":
            args["launchState"] = launchStateEnum.Headless
            continue
        if arg == "-cli":
            args["launchState"] = launchStateEnum.CLI
            continue
        if arg == "-tui":
            args["launchState"] = launchStateEnum.TUI
            continue
        if arg == "-gui":
            args["launchState"] = launchStateEnum.GUI
            continue

        if ("-directory=") in arg:
            keyFile.path = arg.split("=",1)[-1]
            continue
        if ("-id=") in arg:
            keyFile.id = arg.split("=",1)[-1]
            continue
        if ("-password1=") in arg:
            keyFile.password1 = arg.split("=",1)[-1]
            continue
        if ("-password2=") in arg:
            keyFile.password2 = arg.split("=",1)[-1]
            continue
        
        args["cmd"].append(arg)

    return args

if __name__ == "__main__":
    import KeyFile
    keyFile = KeyFile.KeyFile()

    args = parseArgs()

    match(args["launchState"]):
        case launchStateEnum.Headless:
            import Headless
            Headless.main(
                    args["cmd"]
                    )
    match(args["launchState"]):
        case launchStateEnum.CLI:
            print("CLI mode")
    match(args["launchState"]):
        case launchStateEnum.TUI:
            print("TUI mode")
    match(args["launchState"]):
        case launchStateEnum.GUI:
            print("GUI mode")
