import unittest

class TestStegonography(unittest.TestCase):
    
    def setUp(self):
        self.iterationCount = 5

    def testRandomIntegerData(self):
        # Used for stress testing the system for faults.
        import random
        import SteganographyCodec as sc
        
        for j in range(self.iterationCount):
            with self.subTest(j = j):
                originalData = bytes([int(random.random()*255+1) for i in range(int(random.random()*255+1))])+b"\x00"
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

        for j in range(self.iterationCount):
            with self.subTest(j = j):
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

    def setIp(self):
        pass
    
    def testRandomIntegerData(self):
        import TextEncoder as te

        self.assertTrue(True)
        pass

if __name__ == "__main__":
    unittest.main()
