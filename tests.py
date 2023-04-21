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
"""

import unittest
import time
from unittest import mock
from scripts.userfunctions import *
import mp3hash

directories = [
    "./Ken Ashcorp",
    "/Various",
    "./URL Downloads",
    "./GGRIM",
    "./Cxxlion"
]

'''h1 = hashlib.sha256(open(".\\assets\\Testing\\urlinputtest.mp3", "rb")).hexdigest()
path = urlinput("https://www.youtube.com/watch?v=FVjeWMr8aLo")
h2 = hashlib.sha256(open(path, "rb")).hexdigest()'''

def hash(path):
    return mp3hash.mp3hash(path)



class UnitTestingEnvironment(unittest.TestCase):
    def test_unittest_environment(self):
        assert 1 == 1

    def test_hashing_method(self):
        h1 = hash(".\\assets\\Testing\\urlinputtest.mp3")
        h2 = hash(".\\assets\\Testing\\hashingtest.mp3")
        assert h1 != h2

class InputTests(unittest.TestCase):
    @staticmethod
    def test_urlinput():
        h1 = hash(".\\assets\\Testing\\urlinputtest.mp3")
        path = urlinput("https://www.youtube.com/watch?v=FVjeWMr8aLo")
        h2 = hash(path)
        assert h1 == h2

    @mock.patch('scripts.userfunctions.input', create=True)
    def test_input_method(self, mocked_input):
        mocked_input.side_effect = ["./assets/cwant"]
        raise NotImplementedError("")
