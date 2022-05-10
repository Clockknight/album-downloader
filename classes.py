class Information:
    def __init__(self):
        self.release = ''
        self.artist = None
        self.art = ''
        self.cursong = ''

        self.songs = {}
        self.success = {}
        self.history = {}

        # Vars for storing directories to files
        self.histstorage = 'history.json'
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



