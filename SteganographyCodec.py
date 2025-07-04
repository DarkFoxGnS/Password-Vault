from PIL import Image

def write(fileName: str, targetName: str, data: bytes) -> None:
    """
    Writes the data into the files least important bit.

    Params:
        fileName: The name of the base image.
        targetName: The name of the target image.
        data: A byte array which will be encoded into the image.
    """
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
    """
    Reads from the provided file, and returns the decoded byte array.

    Params:
        fileName: The name of the image to read from.
    Returns:
        Byte array containing data.
    """
    with Image.open(fileName) as sourceFile:
        pixels = sourceFile.load()
        width, height = sourceFile.size

        rgbOffset = 0
        bitOffset = 0
        temp = 0
        text = [0]*(width*height*3//8)
        for i in range(width*height*3):

            if i % 8 == 0 and i != 0:
                text[i//8-1] = temp
                temp = 0
            pixelData = pixels[i//3%width,i//3//width][rgbOffset%3] & 1
            temp |= pixelData << (i%8)

            rgbOffset += 1
            bitOffset += 1
    return bytes(text)
