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
        self.histstorage = 'history.json'
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
        self.success.update(infoobj.success)
        self.artist = infoobj.artist

    def historyvar(self):
        return self.artist, self.release, self.histstorage, self.success

    def filterwords(self):
        return self.cursong.split() + self.release.split() + self.artist.split()