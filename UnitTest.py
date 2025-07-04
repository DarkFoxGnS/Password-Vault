import unittest

iterationCount = 5

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
                sc.write("unit.png","encoded-unit.png",originalData)
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
                sc.write("unit.png","encoded-unit.png",originalData)
                readData = sc.read("encoded-unit.png")
                length = 0
                for i in readData:
                    if i == 0:
                        break
                    length+=1

                self.assertEqual(readData[:length], originalData[:-1],originalData.hex())
    def testEmptyData(self):
        import SteganographyCodec as sc

        sc.write("unit.png","encoded-unit.png",b"")
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
        sc.write("unit.png","encoded-unit.png",data)

class TestTextEncoder(unittest.TestCase):

    def setUp(self):
        self.iterationCount = iterationCount
        pass
    
    def testRandomIntegerData(self):
        import DataEncoder as de
        import random
        for _ in range(self.iterationCount):
            with self.subTest():
                originalData = bytes(int(random.random()*254+1) for x in range(int(random.random()*255+1)))
                key = bytes(int(random.random()*254+1) for x in range(int(random.random()*255+1)))
                
                byteData = de.encode(key,originalData)
                
                decodedData = de.decode(key,byteData)
                self.assertEqual(decodedData,originalData,(originalData,decodedData))

    def testRandomStringData(self):
        import DataEncoder as de
        import random

        for _ in range(self.iterationCount):
            with self.subTest():
                originalData = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                password = "".join([chr(int(int(b"1111_11",2)*random.random()+40)) for i in range(1000)])
                
                byteData = de.encode(password.encode(), originalData.encode())
                
                decoded = de.decode(password.encode(), byteData)
                
                self.assertEqual(originalData,decoded.decode(),(originalData,decoded.decode()))
    
    def testEmptyData(self):
        import DataEncoder as de
        
        originalData = b""
        password = b""

        encodedData = de.encode(password,originalData)
        decodedData = de.decode(password,encodedData)
        
        self.assertEqual(originalData,decodedData)

if __name__ == "__main__":
    unittest.main()
