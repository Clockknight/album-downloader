"""
def result():
    io = Information()
    io.historystorage = checkhistory()
    print(readhistory(io))

    searchinput(0, "Ken Ashcorp")
    searchinput(0, "Mystery Skulls")



thing = input("You're running test.py. This is going to clear your history.json, press enter to continue.")

testclear()

searchinput(0, "crowder")
result()

searchinput(0, "Siames")
result()

urlinput("https://www.youtube.com/watch?v=BKUa0ISxhvQ")
searchinput(1, "20 Percent Cooler")
print(readhistory(checkhistory()))

testclear()



class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

if __name__ == '__main__':
    unittest.main()"""

"""
import unittest

from userfunctions import *


class TestingClass(unittest.TestCase):
    def __init__(self, thing):
        clearhistory()
        directories = [
            "./Ken Ashcorp",
            "/Various",
            "./URL Downloads",
            "./GGRIM",
            "./Cxxlion"
        ]

        for dir in directories:
            os.makedirs(dir, exist_ok=True)
            shutil.rmtree(dir)

    def test(self):
        assert 1 == 1

"""


from userfunctions import *

searchinput(0, "Ken Ashcorp")