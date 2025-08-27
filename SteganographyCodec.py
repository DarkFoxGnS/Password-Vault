from PIL import Image

def write(data:bytes, fileName: str, targetName: str) -> None:
    """
    Writes the data into the files least important bit.

    Params:
        fileName: The name of the base image.
        targetName: The name of the target image.
    """
    with Image.open(fileName) as sourceFile:
        pixels = sourceFile.load()
        width,height = sourceFile.size
        
        if width*height < len(data)*8:
            raise Exception("The provided image is too small to contain the data.")

        # Encode the contents of the data into the newly created image.
        rgbSwitch = 0
        bitOffset = 0
        end = len(data)*8
        for i in range(end):
            bitValue = (data[i//8] & (1<<(bitOffset%8))) > 0
            originalPixelValue = list(pixels[i//3%width,i//3//width])
            originalPixelValue[rgbSwitch%3] = (originalPixelValue[rgbSwitch%3] & ~1) | bitValue

            pixels[i//3%width,i//3//width] = tuple(originalPixelValue)

            rgbSwitch += 1
            bitOffset += 1
        
        for i in range(end,width*height*3):
            import secrets
            bitValue = secrets.choice([0,1])
            originalPixelValue = list(pixels[i//3%width,i//3//width])
            originalPixelValue[rgbSwitch%3] = (originalPixelValue[rgbSwitch%3] &  ~1) | bitValue

            pixels[i//3%width,i//3//width] = tuple(originalPixelValue)

            rgbSwitch += 1

        sourceFile.save(targetName,"PNG")

def read(fileName: str,statusQueue:"queue" = None, resultArray:bytearray = None) -> str:
    """
    Reads from the provided file, and returns the decoded byte array.

    Params:
        fileName: The name of the image to read from.
        statusQueue: (Optional) queue being filled with progress. Meant for multiThreading
    Returns:
        Byte array containing data.
    """
    with Image.open(fileName) as sourceFile:
        pixels = sourceFile.load()
        width, height = sourceFile.size

        rgbOffset = 0
        bitOffset = 0
        temp = 0
        size = width*height*3
        text = [0]*(size//8)
        if resultArray is not None:
            resultArray.extend([0]*(size//8))
        for i in range(size):

            if i % 8 == 0 and i != 0:
                text[i//8-1] = temp
                if resultArray is not None:
                    resultArray[i//8-1] = temp
                temp = 0
            pixelData = pixels[i//3%width,i//3//width][rgbOffset%3] & 1
            temp |= pixelData << (i%8)
            
            rgbOffset += 1
            bitOffset += 1
            
            if statusQueue and i%(size//100)==0:
                statusQueue.put(i//(size//100))
    if statusQueue:
        statusQueue.put(100)
    return bytes(text)

def asyncRead(fileName: str):
    import threading, queue
    statusQueue = queue.Queue()
    resultArray = bytearray()
    thread = threading.Thread(target = read, args = (fileName, statusQueue, resultArray))
    thread.start()
    return statusQueue, resultArray
