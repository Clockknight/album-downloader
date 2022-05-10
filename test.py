"""import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()"""

from userfunctions import *
import shutil

clearhistory()

urlinput("https://www.youtube.com/watch?v=BKUa0ISxhvQ")
searchinput(1, "20 Percent Cooler")
searchinput(1, "20 Percent Cooler")
print(readhistory(checkhistory()))
clearhistory()

searchinput(1, "20 Percent Cooler")
searchinput(0, "Ken Ashcorp")
searchinput(0, "kEn AsHCoRp")
print(readhistory(checkhistory()))
clearhistory()