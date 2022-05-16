"""import unittest

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

if __name__ == '__main__':
    unittest.main()"""

from userfunctions import *


def testclear():
    clearhistory()

    test("./Ken Ashcorp")
    test("/Various")
    test("./URL Downloads")
    test("./GGRIM")
    test("./Cxxlion")

    # Hard coded folder remove values for testing purposes


def test(testdir):
    os.makedirs(testdir, exist_ok=True)
    shutil.rmtree(testdir)

'''   
Mystery Skulls
I dont know how but they found me
half alive 
guilty gear xrd
redline OST
fatboy slim 
OK GO
Caravan Palace
Trocadero
The silent comedy
Jamiroquai
The Correspondents
Foster the People
Tame impala
Panic at the Disco
c2c
Jim croce
Franz Ferdinand
Lemon Demon
Devil May Cry OST
Psy
circa waves
st vincent
miike snow
'''

cacheinput()

searchinput(1, "20 Percent Cooler")
update()


searchinput(0, "Lil Boodang")
print(readhistory(checkhistory()))

searchinput(0, "Ken Ashcorp")
print(readhistory(checkhistory()))

urlinput("https://www.youtube.com/watch?v=BKUa0ISxhvQ")
searchinput(1, "20 Percent Cooler")
print(readhistory(checkhistory()))

input("")
testclear()
