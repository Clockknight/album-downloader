class Information:
    def __init__(self):
        self.album = ''
        self.artist = ''
        self.art = ''
        self.cursong = ''

        self.songs = {}
        self.success = {}
        self.history = {}

        # Vars for storing directories to files
        self.histstorage = ''
        self.targetstorage = ''

        self.songcount = 0
        self.totalcount = 0

    def urlinit(self):
        self.album = False
        self.targetstorage = "URL Downloads"

    def summary(self):

        release = {self.artist: self.songs}

        return release


class Settings:
    def __init__(self):
        self.seperatereleases = False
