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



searchinput(1, "20 Percent Cooler")
update()

cacheinput()

searchinput(0, "Lil Boodang")
print(readhistory(checkhistory()))

searchinput(0, "Ken Ashcorp")
print(readhistory(checkhistory()))

urlinput("https://www.youtube.com/watch?v=BKUa0ISxhvQ")
searchinput(1, "20 Percent Cooler")
print(readhistory(checkhistory()))

input("")
testclear()
