"""import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()"""

from userfunctions import *
import shutil

urlinput("https://www.youtube.com/watch?v=BKUa0ISxhvQ")

searchinput(1, "20 Percent Cooler")
searchinput(0, "Ken Ashcorp")
clearhist()

searchinput(0, "kEn AsHCoRp")
clearhist()