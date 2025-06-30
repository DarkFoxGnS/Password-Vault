from PIL import Image

def write(fileName: str, targetName: str, data: bytes) -> None:
    """
    Writes the data into the files least important bit.

    Params:
        fileName: The name of the base image.
        targetName: The name of the target image.
        data: A byte array which will be encoded into the image.
    """
    print(data,"\n",data.hex())
    with Image.open(fileName) as sourceFile:
        pixels = sourceFile.load()
        width,height = sourceFile.size
        
        if width*height < len(data)*8:
            raise Exception("The provided image is too small to contain the data.")

        # Encode the contents of the data into the newly created image.
        rgbSwitch = 0
        bitOffset = 0
        for i in range(len(data)*8):
            bitValue = (data[i//8] & (1<<(bitOffset%8))) > 0
            originalPixelValue = list(pixels[i//3%width,i//3//width])
            originalPixelValue[rgbSwitch%3] = (originalPixelValue[rgbSwitch%3] & ~(1 << 0)) | ((bitValue & 1) << 0)

            pixels[i//3%width,i//3//width] = tuple(originalPixelValue)

            rgbSwitch += 1
            bitOffset += 1
        sourceFile.save(targetName,"PNG")

def read(fileName: str) -> str:

    with Image.open(fileName) as sourceFile:
        pixels = sourceFile.load()
        width, height = sourceFile.size

        rgbOffset = 0
        bitOffset = 0
        temp = 0
        text = b""
        for i in range(width*height*3):
            if i % 8 == 0 and i != 0:
                if temp == 0:
                    print(text)
                    break
                print("\t",format(temp,"08b"))
                text += temp.to_bytes()
                temp = 0
            pixelData = pixels[i//3%width,i//3//width][rgbOffset%3] & 1
            temp |= pixelData << (i%8)
            print(format(pixels[i//3%width,i//3//width][rgbOffset%3],"08b"),pixelData, format(pixelData<<(i%8)))
            # print(f"{i//8}/{width*height*3//8}",pixels[i//3%width,i//3//width][rgbOffset%3],pixelData,pixelData << 7-(i%8),format(temp,"08b"),chr(temp))

            rgbOffset+=1
            bitOffset

if __name__ == "__main__":
    choice = input("(W)rite or (R)ead: ")
    match(choice):
        case "w" | "W":
            # filename = input("File to open: ")
            # text = input("Data to encode into file: ")
            # text += b"\x00".decode()
            
            filename = "fox.png"
            text = "Hello World"

            write(filename,f"encoded-{filename}",text.encode())
        case "r" | "R":
            filename = "encoded-fox.png"
            read(filename)
