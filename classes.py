class Information:
    def __init__(self):
        self.album = ''
        self.artist = ''
        self.art = ''
        self.dirstorage = ''
        self.history = {}
        self.cursong = ''

        self.songs = []

        self.songcount = 0
        self.totalcount = 0

    def urlinit(self):
        self.album = False
        self.dirstorage = "URL Downloads"


class Settings:
    def __init__(self):
        self.seperatealbums = False
