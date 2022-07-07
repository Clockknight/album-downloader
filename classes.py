class Information:
    def __init__(self):
        self.release = ''
        self.art = ''
        self.cursong = ''
        self.artist = None
        self.album = True

        self.songs = {}
        self.success = {}
        self.history = {}

        # Vars for storing directories to files
        self.histstorage = './assets/history.json'
        self.targetstorage = ''

        self.songcount = 0
        self.totalcount = 0

    def init(self):
        self.album = False
        self.targetstorage = "URL Downloads"

    def summary(self):

        release = {self.artist: self.songs}

        return release

    def update(self, infoobj):
        """Update values of the success dict variable with new """
        self.success.update(infoobj.success)
        self.artist = infoobj.artist

    def historyvar(self):
        """Return various variables used when writing to history.json"""
        return self.histstorage, {self.artist: self.success}

    def filterwords(self):
        """Return words that are used when filtering out video results"""
        return self.artist.split() + self.release.split()
