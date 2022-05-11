"""import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()"""

from userfunctions import *

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
clearhistory()