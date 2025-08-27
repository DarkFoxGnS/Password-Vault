SCENES = []

class SceneEnum():
    Main = 0
    New = 1
    Load = 2
    SelectDirectory = 3
    IdInput = 4
    Password1Input = 5
    Password2Input = 6
    LoadProgress = 7
    PasswordPage = 8
    DecodeProgress = 9
    

def help() -> None:
    print("\nHelp:")
    for command in globalFunctions.items():
        print("\t",command[0],":",command[1][1])
    for command in SCENES[-1].functions.items():
        print("\t",command[0],":",command[1][1])
    input("\nPress ENTER to continue...")

def back() -> None:
    if len(SCENES) > 1:
        del SCENES[-1]

def menu() -> None:
    for i in range(len(SCENES)-1,0,-1):
        del SCENES[i]

def shutdown() -> None:
    exit()

globalFunctions = {
            "back":[back,"Goes back to the previous menu."],
            "menu":[menu,"Goes back to the main menu."],
            "exit":[shutdown,"Closes the application."],
            "help":[help,"Prints out the available commands."],
        }

class UIObject():
    def __init__(self,**kwargs:"text: String, functions: Dictionary"):
        self.waitForUser = True
        self.text = kwargs.get("text","")
        self.functions = kwargs.get("functions",{})
    
    def update(self,userInput) -> bool:
        function = self.functions.get(userInput.lower(),False)
        if function:
            function[0]()
            return True
        function = globalFunctions.get(userInput.lower(),False)
        if function:
            function[0]()
            return True
        return False

    def draw(self):
        print(self.text)

    def returns(self,args):
        pass

class UIInputObject(UIObject):
    def __init__(self,**kwargs:"text: String, functions: Dictionary, target: String"):
        super().__init__(**kwargs)
        self.text = kwargs.get("text","")
        self.target = kwargs.get("target","")

    def update(self,userInput):
        SCENES[-2].returns({self.target:userInput})
        back()

class UIInputNumberObject(UIInputObject):
    def update(self,userInput):
        if userInput.isnumeric():
            super().update(userInput)
        else:
            print("Number only!")

class UIArgumentedObject(UIObject):

    def __init__(self,**kwargs:"text: String, functions: Dictionary, arguments: Array"):
        super().__init__(**kwargs)
        self.arguments = {}
        for arg in kwargs.get("arguments",[]):
            self.arguments[arg] = None

    def draw(self):
        super().draw()
        for arg in self.arguments:
            print(arg,"=",self.arguments.get(arg))
        print("")
    
    def returns(self,args):
        for key in args:
            if key in self.arguments:
                self.arguments[key] = args.get(key)

class UIProgress(UIObject):
    def __init__(self, **kwargs:"text:String, queue: queue"):
        super().__init__(**kwargs)
        self.waitForUser = False
        self.queue = kwargs.get("queue")
        self.value = 0
        self.successFunc = kwargs.get("successFunc",back)
        self.failureFunc = kwargs.get("failureFunc",back)

    def draw(self):
        print(self.text,self.value,"%")

    def update(self, userInput):
        if not self.queue:
            self.failureFunc()
            return
        self.value = self.queue.get()
        if self.value == 100:
            self.successFunc()


###########################
# UI Instantiation functions

def initMain():

    def newFunction():
        initScene(SceneEnum.New)

    def loadFunction():
        initScene(SceneEnum.Load)

    return UIObject(
        text="""
Password-Vault, by Tibor Péter Szabó.
\tType \"New\" to create a new file.
\tType \"Load\" to load an existing file.
\tType \"Exit\" to leave the application.
\tType \"Help\" to read available commands.
        """,
        functions = {
            "new":[newFunction,"Creates a new password vault file."],
            "load":[loadFunction,"Load an existing password file."],
            }
        )

def initNew():
    raise Exception("Not yet implemented.")

def initLoad():
    def dirFunction():
        initScene(SceneEnum.SelectDirectory)

    def idFunction():
        initScene(SceneEnum.IdInput)

    def password1Function():
        initScene(SceneEnum.Password1Input)

    def password2Function():
        initScene(SceneEnum.Password2Input)
    
    def loadFunction():
        import KeyFile
        arguments = SCENES[-1].arguments #Will always be and UIArgumentedObject
        KeyFile.KeyFile(
                arguments.get("directory"),
                arguments.get("id"),
                arguments.get("password1"),
                arguments.get("password2"),
                )
        initScene(SceneEnum.LoadProgress)

    return UIArgumentedObject(
        text = """
Load file:
Enter parameter name to edit it.
        """,
        arguments = [
            "directory",
            "id",
            "password1",
            "password2",
            ],
        functions = {
            "directory":[dirFunction,"Select the password directory."],
            "id":[idFunction,"Input the ID of the password file."],
            "password1":[password1Function,"Input password1 for the file."],
            "password2":[password2Function,"Input password2 for the file."],
            "load":[loadFunction,"Opens the password file using the given credentials."]
            }
            )

def initSelectDirectory():
    def y():
        from tkinter import filedialog
        selectedDir = filedialog.askdirectory(initialdir=".\passwords")
        if selectedDir is not "":
            SCENES[-2].returns({"directory":selectedDir})
        back()

    def n():
        back()

    return UIObject(
            text = "Open File Explorer? [Y/N]",
            functions ={
                "y":[y,"Yes"],
                "n":[n,"No"],
                },
            )

def initIdInput():
    return UIInputNumberObject(
            text = "Enter the ID of the correct password file:",
            target = "id",
            )

def initPassword1Input():
    return UIInputObject(
            text = "Enter Password1:",
            target = "password1",
            )

def initPassword2Input():
    return UIInputObject(
            text = "Enter Password2:",
            target = "password2",
            )

def initLoadProgress():

    def loadedFunction():
        menu()
        initScene(SceneEnum.PasswordPage)

    import KeyFile
    keyFile = KeyFile.KeyFile.getKeyFile()
    return UIProgress(
            text = "Loading",
            queue = keyFile.loadFile(True),
            successFunc = loadedFunction,
            )

def initPasswordPage():
    return UIObject(text="Passwords presented here")

###########################

def initScene(sceneID: int):
    scene = None
    match(sceneID):
        case SceneEnum.Main:
            scene = initMain()
        case SceneEnum.New:
            scene = initNew()
        case SceneEnum.Load:
            scene = initLoad()
        case SceneEnum.SelectDirectory:
            scene = initSelectDirectory()
        case SceneEnum.IdInput:
            scene = initIdInput()
        case SceneEnum.Password1Input:
            scene = initPassword1Input()
        case SceneEnum.Password2Input:
            scene = initPassword2Input()
        case SceneEnum.LoadProgress:
            scene = initLoadProgress()
        case SceneEnum.PasswordPage:
            scene = initPasswordPage()
        case SceneEnum.DecodeProgress:
            scene = initDecodeProgress()
    if not scene:
        raise Exception(f"SceneID:{sceneID} not existent!")
    SCENES.append(scene)

def init():
    initScene(SceneEnum.Main)

def update():
    while(True):
        SCENES[-1].draw()
        if SCENES[-1].waitForUser:
            userInput = input("> ")
        SCENES[-1].update(userInput)
