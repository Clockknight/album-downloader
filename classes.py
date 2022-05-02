class Information:
    def __init__(self):
        self.album = ''
        self.artist = ''
        self.art = ''
        self.cursong = ''


        self.songs = {}

        #Vars for storing directories to files
        self.histstorage = ''
        # TODO rename .dirstorage into something less generic
        self.dirstorage = ''

        self.songcount = 0
        self.totalcount = 0

    def urlinit(self):
        self.album = False
        self.dirstorage = "URL Downloads"

    def summary(self):

        release = {self.artist: self.songs}

        return release


class Settings:
    def __init__(self):
        self.seperatereleases = False
