class KeyFile():
    _instance = None
    def __new__(cls,*args,**kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def getKeyFile():
        if KeyFile._instance:
            return KeyFile._instance
        else:
            raise Exception("KeyFile was not initialised!")
    
    def __init__(self):
        self.path = None
        self.id = None
        self.password1 = None
        self.password2 = None
        self.data = None

    def loadFile(self, threaded = False):
        import SteganographyCodec, os
        fileName = f"{self.path}\\{self.id}.png"
        
        try:
            open(fileName,"r")
        except:
            print("Invalid file path!")
            exit()

        if threaded:
            q, self.data = SteganographyCodec.asyncRead(fileName)
            return q
        else:
            self.data = SteganographyCodec.read(fileName)

    def saveFile(self, threaded = False):
        import SteganographyCodec
        fileName = f"{self.path}\\{self.id}.png"
        SteganographyCodec.write(self.data,fileName, fileName)

    def decode(self, threaded = False):
        import DataCodec as dc
        self.data = dc.decode(self.password1, self.password2, self.data)

    def encode(self, threaded = False):
        import DataCodec as dc
        self.data = dc.encode(self.password1, self.password2, self.data)
    
    def serialize(self,array:"array"):
        self.data = b""
        for elem in array:
            name = elem[0]
            pasw = elem[1]
            self.data+=name.encode()+b"\0"+pasw.encode()+b"\0\0"
        if len(array) == 0:
            self.data+=b"\0\0"
        self.data+=b"\0"

    def parse(self):
        array = []
        password = []
        start = 0
        end = 0
        zeroCounter = 0

        for i in self.data:
            if i == 0:
                zeroCounter+=1
                if zeroCounter == 1:
                    password.append(bytes(self.data[start:end]).decode())
                    start = end+1
                if zeroCounter == 2:
                    if len(password) == 2:
                        array.append(password)
                    password = []
                    start = end+1
                if zeroCounter == 3:
                    return array
            else:
                zeroCounter = 0
            end+=1

