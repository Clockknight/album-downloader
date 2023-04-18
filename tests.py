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
from unittest import mock
from userfunctions import *

directories = [
    "./Ken Ashcorp",
    "/Various",
    "./URL Downloads",
    "./GGRIM",
    "./Cxxlion"
]

class TestingClass(unittest.TestCase):

    '''def __init__(self, test):
        clearhistory()


        for dir in directories:
            os.makedirs(dir, exist_ok=True)
            shutil.rmtree(dir)

        pass'''

    @mock.patch('userfunctions.input', create=True)
    def test_urlinput(self, mocked_input):
        mocked_input.side_effect = ["./assets/cwant"]

        # download audio before running this script
        # get hash somehow

        # inside of script
        # urlinput()
        # get download
        # get ITS hash somehow
        # assert compare is equal

        pass
    @mock.patch('userfunctions.input', create=True)
    def test2(self, mocked_input):
        mocked_input.side_effect = ["./assets/cwant"]

        assert 1==1
        pass




