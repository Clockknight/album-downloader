import os
import userfunctions


class Information:
    def __init__(self):
        self.album = ''
        self.art = ''
        self.current_song = ''
        self.artist = None
        self.clean_artist = self.artist  # variable to remove () from end of artists when they have a commonly used name
        self.is_album = True

        self.songs = {}
        self.success = {self.album: {}}
        self.history = {}

        # Vars for storing directories to files
        self.history_storage = './assets/history.json'
        self.target_storage = ''

        self.song_count = 0
        self.total_count = 0

        self.test_mode = False

    def setup_test(self):
        self.history_storage = "./test/history.json"
        self.target_storage = "./test/"
        self.test_mode = True

    def setup_url(self):
        self.is_album = False
        self.target_storage += "URL Downloads"

    def update(self, infoobj):
        """Update values of the success dict variable with new """
        self.success.update(infoobj.success)
        self.artist = infoobj.artist

    def history_variables(self):
        """Return various variables used when writing to history.json"""
        return self.history_storage, {self.artist: {self.album: self.success}}

    def filter_words(self):
        """Return words that are used when filtering out video results"""
        return self.clean_artist.split(), self.album.split() + self.current_song.split()

    def set_artist(self, given_artist):
        self.artist = given_artist
        self.clean_artist = given_artist  # TODO remove (n) when it's present at the end of the artist variable
        self.history = {given_artist: {}}

    def update_success(self, newdict):
        if self.success == {"": {}}:
            self.success = newdict
        else:
            self.success.update(newdict)

    def set_storage(self):
        """


        """
        download_path = "Downloads"
        if self.test_mode:
            download_path = os.path.join("./Test", download_path)
        self.target_storage = os.path.join(download_path, userfunctions.writable(self.artist),
                                           userfunctions.writable(self.album))
