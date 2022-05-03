class Information:
    def __init__(self, settings=None):
        if settings is None:
            settings = Settings()
        self.release = ''
        self.artist = ''
        self.art = ''
        self.cursong = ''

        self.songs = {}
        self.success = {}
        self.history = {}

        # Vars for storing directories to files
        self.histstorage = settings.gethistdir()
        self.targetstorage = ''

        self.songcount = 0
        self.totalcount = 0

    def init(self, mode):
        match mode:
            case "url":
                self.album = False
                self.targetstorage = "URL Downloads"

    def summary(self):

        release = {self.artist: self.songs}

        return release


class Settings:
    def __init__(self):
        self.seperatereleases = False
        self.histdir = 'history.json'

    def gethistdir(self):
        return self.histdir
