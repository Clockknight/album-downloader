

import unittest
import time
from unittest import mock
from userfunctions import *
import mp3hash

class UnitTestingEnvironment(unittest.TestCase):
    def test_unittest_environment(self):
        assert 1 == 1

    def test_hashing_method(self):
        h1 = mp3hash.mp3hash('assets/Testing/urlinputtest.mp3')
        h2 = mp3hash.mp3hash('assets/Testing/hashingtest.mp3')
        h3 = mp3hash.mp3hash('assets/Testing/urldouble.mp3')
        assert h1 != h2 and h1 == h3

class InputTests(unittest.TestCase):
    @staticmethod
    def test_urlinput():
        h1 = mp3hash.mp3hash("./assets/Testing/urlinputtest.mp3")
        path = url_input("https://www.youtube.com/watch?v=FVjeWMr8aLo")
        h2 = mp3hash.mp3hash(path)
        assert h1 == h2

    @mock.patch('scripts.userfunctions.input', create=True)
    def test_input_method(self, mocked_input):
        mocked_input.side_effect = ["./assets/cwant"]
        raise NotImplementedError()

    def test_cacheinput(self):
        raise NotImplementedError()

    def test_searchinput(self):
        raise NotImplementedError()



class MethodTests(unittest.TestCase):
    #TODO implement all the tests for this class
    def test_update(self):
        raise NotImplementedError()

    def test_redownload(self):
        raise NotImplementedError()

    def test_searchprocess(self):
        raise NotImplementedError()

    def test_parseartist(self):
        raise NotImplementedError()

    def test_parseartistpage(self):
        raise NotImplementedError()

    def test_processrelease(self):
        raise NotImplementedError()

    def test_downloadlistofsongs(self):
        raise NotImplementedError()

    def test_downloadsong(self):
        raise NotImplementedError()

    def test_tagsong(self):
        raise NotImplementedError()
