"""import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()"""

from userfunctions import *

searchinput(0, "Lil Boodang")
print(readhistory(checkhistory()))
searchinput(0, "LiL BoOdaNg")
print(readhistory(checkhistory()))
clearhistory()

searchinput(0, "Ken Ashcorp")
print(readhistory(checkhistory()))
searchinput(0, "KeN aShCorP")
print(readhistory(checkhistory()))
clearhistory()


urlinput("https://www.youtube.com/watch?v=BKUa0ISxhvQ")
searchinput(1, "20 Percent Cooler")
searchinput(1, "20 Percent Cooler")
print(readhistory(checkhistory()))
clearhistory()