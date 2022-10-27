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

    def urlsetup(self):
        self.isalbum = False
        self.targetstorage = "URL Downloads"

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

    def setartist(self, inartist):
        self.artist = inartist
        self.history = {inartist: {}}

    def updatesuccess(self, newdict):
        if self.success == {"": {}}:
            self.success = newdict
        else:
            self.success.update(newdict)
