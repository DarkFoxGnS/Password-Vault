from KeyFile import KeyFile

def main(command:"array"):
    if len(command) == 0:
        print("Commands were not provided!")
        exit()

    keyFile = KeyFile.getKeyFile()
    
    if command[0] == "keygen":
        keyGen(command)
        exit()

    if keyFile.path == None:
        print("Directory was not provided!\n\tUse -directory flag to provide a directory.\n\tFor example: -directory=passwords\\exampleDir")
        exit()
    if keyFile.id == None:
        print("ID was not provided!\n\tUse -id flag to provide the id.\n\tFor example: -id=5")
    if keyFile.password1 == None:
        print("Password1 was not provided!\n\t Use -password1 flag to provide a password.\n\tFor example: -password1=ExamplePassword123")
        exit()

    if command[0] == "new":
        new(keyFile, command)
        return
    
    load(keyFile)
    
    match(command[0]):
        case "list":
            list(keyFile)
        case "add":
            add(keyFile,command)
        case "get":
            get(keyFile, command)
        case "del":
            delete(keyFile, command)

def keyGen(command):
    import KeyForge
    if len(command) == 1:
        print("Invalid syntax!\n\tPlease use:\n\t\"keygen <length>\"\n\tOR\n\t\"keygen <length> <charaterSet>\"\nExample:\n\t\"keygen 15\" -> 2TNFd~ohb|\'7>G]\n\t\"keygen 15 A-Za-z0-9?!\\\\-= \"-> vk-4KP\\SUoNV?1VL7>")
        exit()
    length = int(command[1])
    if len(command) == 2:
        print(KeyForge.generate(length))
    else:
        characteSet = command[2]
        print(KeyForge.generateCustom(characteSet,length))


def add(keyFile: KeyFile, command: "array"):
    if len(command) != 3:
        print("Invalid syntax!\n\tPlease use:\n\t\"add <Name> <Password>\".")
        exit()

    data = keyFile.parse()
    data.append([command[1],command[2]])
    keyFile.serialize(data)
    keyFile.encode()
    keyFile.saveFile()

def delete(keyFile:KeyFile, command:"array"):
    if len(command) != 2:
        print("Invalid syntax%\nPlease use:\n\tdel <password_name>")
        exit()
    target = command[1]
    data = keyFile.parse()
    for passw in data:
        if passw[0] == target:
            data.remove(passw)

    keyFile.serialize(data)
    keyFile.encode()
    keyFile.saveFile()

def get(keyFile: KeyFile, command: "array"):
    if len(command) != 2:
        print("Invalid syntax!\n\tPlease use:\n\t\"get <Password name>\".")
        exit()
    data = keyFile.parse()
    name = command[1]
    for elem in data:
        if elem[0] == name:
            print(elem[1])

def list(keyFile: KeyFile):
    data = keyFile.parse()
    print(f"Passwords stored in the file ({len(data)}):")
    for passw in data:
        print(passw[0])

def new(keyFile:KeyFile, command: "array"):
    import SteganographyCodec as sc
    import os

    if len(command) != 3:
        print("Invalid syntax!\nPlease use:\n\tnew <original image> <number of password files>")
        exit()
    try:
        os.mkdir(keyFile.path)
        print("Creating directory:", keyFile.path)
    except Exception as e:
        print("Directory", keyFile.path, "already exists, continuing.")
    
    origin = command[1]
    instanceCount = int(command[2])
    
    for i in range(instanceCount):
        print(f"Creating password file: {keyFile.path}\\{i}.png",end="")

        if i == int(keyFile.id):
            keyFile.data = b"\0\0\0"
            keyFile.encode()
            sc.write(keyFile.data,origin,f"{keyFile.path}\\{keyFile.id}.png")
        else:
            sc.write(b"", origin, f"{keyFile.path}\\{i}.png")
        print(" Done")

def load(keyFile:KeyFile):
    if keyFile.id == None:
        print("ID was not provided!\n\tUse -id flag to provide an ID for the password file.\n\tFor example: -id=5")
        exit()
    keyFile.loadFile()
    keyFile.decode()
