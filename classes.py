import os

import userfunctions


class Information:
    def __init__(self):
        self.album = ''
        self.art = ''
        self.cursong = ''
        self.artist = None
        self.cleanartist = self.artist  # variable to remove () from end of artists when they have a commonly used name
        self.isalbum = True

        self.songs = {}
        self.success = {self.album: {}}
        self.history = {}

        # Vars for storing directories to files
        self.histstorage = './assets/history.json'
        self.targetstorage = ''

        self.songcount = 0
        self.totalcount = 0


    def SetupTest(self):
        self.histstorage = "./test/history.json"
        self.targetstorage = "./test/"

    def urlsetup(self):
        self.isalbum = False
        self.targetstorage += "URL Downloads"

    def update(self, infoobj):
        """Update values of the success dict variable with new """
        self.success.update(infoobj.success)
        self.artist = infoobj.artist

    def historyvar(self):
        """Return various variables used when writing to history.json"""
        return self.histstorage, {self.artist: {self.album: self.success}}

    def filterwords(self):
        """Return words that are used when filtering out video results"""
        return self.cleanartist.split(), self.album.split() + self.cursong.split()

    def setArtist(self, given_artist):
        self.artist = given_artist
        self.cleanartist = given_artist  #TODO remove (n) when it's present at the end of the artist variable
        self.history = {given_artist: {}}

    def updatesuccess(self, newdict):
        if self.success == {"": {}}:
            self.success = newdict
        else:
            self.success.update(newdict)

    def setStorage(self):
        self.targetstorage = os.path.join(self.targetstorage, "Downloads", userfunctions.writable(self.artist), userfunctions.writable(self.album))

