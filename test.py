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

def result():
    io = Information()
    io.historystorage = checkhistory()
    print(readhistory(io))

thing = input("You're running test.py. This is going to clear your history.json, press enter to continue.")

testclear()

searchinput(0, "crowder")
result()

searchinput(0, "Siames")
result()

'''
urlinput("https://www.youtube.com/watch?v=BKUa0ISxhvQ")
searchinput(1, "20 Percent Cooler")
print(readhistory(checkhistory()))'''

testclear()
