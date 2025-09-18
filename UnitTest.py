import unittest
import _io

iterationCount = 100

class TestStegonography(unittest.TestCase):
    
    def setUp(self):
        self.iterationCount = iterationCount

    def testRandomIntegerData(self):
        # Used for stress testing the system for faults.
        import random
        import SteganographyCodec as sc
        
        for _ in range(self.iterationCount):
            with self.subTest():
                # Random data between 1-255
                originalData = bytes([int(random.random()*254+1) for i in range(int(random.random()*255+1))])+b"\x00"
                sc.write(originalData,"unit.png","encoded-unit.png")
                readData = sc.read("encoded-unit.png")
                length = 0
                for i in readData:
                    if i == 0:
                        break
                    length+=1
                
                self.assertEqual(readData[:length], originalData[:-1],originalData.hex())
    
    def testRandomStringData(self):
        import random
        import SteganographyCodec as sc

        for _ in range(self.iterationCount):
            with self.subTest():
                originalData = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)]).encode()+b"\x00"
                sc.write(originalData,"unit.png","encoded-unit.png")
                readData = sc.read("encoded-unit.png")
                length = 0
                for i in readData:
                    if i == 0:
                        break
                    length+=1

                self.assertEqual(readData[:length], originalData[:-1],originalData.hex())
    def testEmptyData(self):
        import SteganographyCodec as sc

        sc.write(b"","unit.png","encoded-unit.png")
        # Only happens if sc.write doesn't fail.
        self.assertTrue(True)

    @unittest.expectedFailure
    def testFullData(self):
        import SteganographyCodec as sc
        from PIL import Image

        image = Image.open("unit.png")
        width,height = image.size
        image.close()
        data = bytes(width*height*3)
        sc.write(data,"unit.png","encoded-unit.png")

class TestTextCodec(unittest.TestCase):

    def setUp(self):
        self.iterationCount = iterationCount
        pass

    def testRandomStringData(self):
        import DataCodec as de
        import random

        for _ in range(self.iterationCount):
            with self.subTest():
                originalData = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                password1 = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                password2 = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                
                byteData = de.encode(password1, password2, originalData.encode())
                
                decoded = de.decode(password1, password2, byteData)
                
                self.assertEqual(originalData,decoded.decode(),(originalData,decoded.decode()))
    
    def testOnlyPassword1(self):
        import DataCodec as de
        import random
        for _ in range(self.iterationCount):
            with self.subTest():
                originalData = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                password1 = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                encodedData = de.encode(password1, None, originalData.encode())
                decodedData = de.decode(password1, None, encodedData)
                
                self.assertEqual(originalData,decodedData.decode(),(originalData,decodedData.decode()))

    def testEmptyData(self):
        import DataCodec as de
        
        originalData = b""
        password1 = ""
        password2 = ""

        encodedData = de.encode(password1, password2 ,originalData)
        decodedData = de.decode(password1, password2 ,encodedData)
        
        self.assertEqual(originalData,decodedData)

class TestKeyFile(unittest.TestCase):
    def setUp(self):
        self.iterationCount = iterationCount

    def testKeyFileSerialize(self):
        import KeyFile
        import random
        keyFile = KeyFile.KeyFile()
        for _ in range(self.iterationCount):
            with self.subTest():
                baseData = [
                        [
                            "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)]),
                            "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)]),
                        ],[
                            "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)]),
                            "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)]),
                        ]]
                keyFile.serialize(baseData)
                self.assertEqual(baseData,keyFile.parse())
    
    def testKeyFileEncodeDecode(self):
        import KeyFile
        import random
        keyFile = KeyFile.KeyFile()
        for _ in range(self.iterationCount):
            with self.subTest():
                baseData = b"Name\0Password\0\0\0"
                keyFile.data = baseData
                keyFile.password1 = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                keyFile.password2 = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                keyFile.encode()
                keyFile.decode()
                self.assertEqual(baseData, keyFile.data)

class DummyStream(_io.TextIOWrapper):
    def __init__(self,file,original):
        super().__init__(original)
        self.file = file
        self.original = original

    def write(self,text):
        self.file.write(text)
        self.original.write(text)

if __name__ == "__main__":
    import sys
    file = open("UnitTestResult.txt","w")
    sys.stdout = DummyStream(file,sys.stdout)
    sys.stderr = DummyStream(file,sys.stderr)
    print("Testing with",iterationCount,"cycles.")
    unittest.main(verbosity=3)
