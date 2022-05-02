from json import JSONDecodeError

import eyed3
import urllib
import requests
import shutil
import pytube

from pytube import YouTube, Search
from bs4 import BeautifulSoup
from moviepy.editor import *
from classes import *
from helperfunctions import *
from pydub import AudioSegment, effects

def optionselect():
    """Text menu for user to choose option"""
    option = input('''
Welcome to Clockknight's Album Downloader. Please choose from an option below by entering the option number:

1) Cache Mode {Not Implemented}
Provide a .txt file with links to album's google result pages, seperated by lines.

2) Search Mode (Artist)
Search for an artist's discography. The artist's discography will be stored in history.json

3) Search Mode (Album)
Search for an album. Recommended for albums with generic artist like "Various".

4) Update {Not Implemented}
Will check for new releases from artists that you have used this script to look at before. 

8) URL Mode
Paste in a YouTube URL, and the program will download it.

9) Settings
Change the settings of the script.

0) Exit

    ''')

    match option:
        case '1':
            cacheinput()
        case '2':
            searchinput(0, "")
        case '3':
            searchinput(1, "")
        case '4':
            update()
        case '8':
            urlinput()
        case '9':
            print("Not implemented yet, sorry")
        case '0':
            sys.exit()
        case _:
            print('Invalid option selected. Please try again.\n\n')


# Functions that take input from user, pass release pages onto parse functions

def cacheinput():
    """Take multiple inputs from text file, ask user if given input is artist or release."""
    # TODO implement cacheinput
    # needs to refer to clockknight want.txt, and then run
    # parses each line as new input, prompts user to clarify if each line is an artist or a user
    # if it is a url, note it and move on instead of actually asking
    # Find text file with links to google searches of albums' songs
    filedir = input(
        'Please enter the directory of the text file that has the links to appropriate files separated by newlines.\n')

    # Use readlines to seperate out the links of albums
    cachearray = open(filedir, 'r').readlines()
    # Run downloadlistofsongs
    # for item in resultArray:
    # ask user if its artist or album
    # store information in related array

    # after for loop, call releaseinput() or artistinput() based on inputs given before


def urlinput():
    """Download given YouTube URL as MP3."""
    # TODO replace all instance of infoobject with reference to a Information class
    infoobject = Information().urlinit()
    # TODO rename .dirstorage into something less generic
    os.makedirs(infoobject.dirstorage, exist_ok=True)  # Make the folder
    url = input('\nPlease input the url of the video you want to download.\n\t')

    try:
        # Declare ytobj now to declare infoobject.art as the youtube thumbnail
        ytobj = YouTube(url)
        infoobject.art = ytobj.thumbnail_url
        downloadsong(ytobj, infoobject)
    except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:
        input("Invalid URL. Press Enter to return to the main menu.")


def searchinput(mode, searchterm):
    """Get user input for release or artist to search, then search it."""
    word = "artist"
    if mode == 1:
        word = "release"

    # Get input for artist/album name when no term is passed
    if searchterm == "":
        searchterm = input('\nPlease input the name of the ' + word + ' you want to search for.\n\t')

    searchprocess(word, searchterm)  # call helper function


# Functions to parse information


def searchprocess(word, searchterm):
    """Parse relevant information and call to appropriate function."""
    resultartiststhatarentmatching = []
    searchterm = searchterm.lower()
    urlterm = urllib.parse.quote_plus(searchterm)  # Makes artist string OK for URLs
    query = 'https://www.discogs.com/search/?q=' + urlterm + '&type=' + word  # makes url to search for results
    page = requests.get(query)

    # Codeblock to try and find albums based on mode provided
    soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it

    # Creates a list from all the divs that make up the cards
    divlist = soup.find_all('div', {"class": "card_large"})

    # Go through each div, each one has a release/artist with a link out
    for div in divlist:
        # TODO Give up and print a bunch of results if no perfect match is found

        # TODO Check if multiple versions from different artists exist, get one with most songs
        result = div.find('h4').find('a')['title'].lower()
        if result == searchterm:  # compare input to card's title
            # TODO run on more than first release matched (get every unique song title returned)
            # Run different function mode chosen
            match word:
                case 'release':
                    success = processrelease("https://discogs.com" + div.a["href"])
                    # TODO Make Fail case here (would mean first page has 0 matches)

                case 'artist':
                    # Only artist mode has multipage support (Not an issue yet?)
                    success = parseartist("https://discogs.com" + div.a["href"] + "?page=")
                    # TODO Make this write to json just the artist, since no results were found




            # After above search runs, write to the history json then break
            # Both return a success object
            writehistory(success)
            break

    # Should print out unique results scraped, and give user chance to correct input


def parseartist(query):
    """Parse artist, calling parseartistpage for each page. Return formatted list of songs downloaded."""
    # TODO include method to get releases the artist is only credited in
    index = 1
    success = {}

    while True:
        # store array of releases to download
        try:
            releases = parseartistpage(query + str(index))
        except AttributeError as e:
            break

        # if nothing is returned from above, break out (query for parseartistpage was an empty page)
        if not releases:
            break
        for release in releases:
            success.update(processrelease(release))
        # go to next page of artist
        index += 1

    return success


def parseartistpage(query):
    """Parse a single page of releases on an artist's page. Return array of release URLs."""
    results = []
    soup = requests.get(query)
    soup = BeautifulSoup(soup.text, "html.parser")

    # < table class ="cards table_responsive layout_normal" id="artist" >
    trs = soup.find("table", id="artist").find_all("tr")
    for tr in trs:
        # Every tr with an album has this attribute
        if tr.has_attr("data-object-type"):
            tr = tr.find("a")
            results.append("https://discogs.com" + tr["href"])

    return results


def processrelease(query):
    """Parse information for release and send to downloadlistofsongs. Return formatted dict of success songs."""
    # TODO Figure out how to deal with multiple releases with the same name EG madeon - adventure
    infoobject = Information()
    infoobject.histstorage = checkhistory()

    #  tryexcept for passed query
    try:
        page = requests.get(query)  # Use requests on the new URL
        soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
    except:
        print('Error: failure processing album. Link provided - ' + query)
        return

    name = soup.find('h1', {"class", "title_1q3xW"})  # grabs artist and album
    artistname = name.find('a').text
    infoobject.artist = artistname  # separate artist
    infoobject.album = name.text[len(artistname) + 3:]  # grab album by removing enough characters from above var

    print('\n\tDownloading Album - ' + infoobject.album)
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the <a> tag of the cover preview
    try:
        infoobject.art = requests.get("https://discogs.com" + coverart.find('a')['href'])
    except:
        # Let the user know the album art isn't available
        print('\t\tWarning: Problem getting album art - ' + infoobject.album)
        infoobject.art = 'fail'  # set it to fail for mp3 tag check

    # Preparing directory to download song
    # create folder for artist, and subfolder for release
    infoobject.dirstorage = os.path.join(writable(infoobject.artist), writable(infoobject.album))
    os.makedirs(infoobject.dirstorage, exist_ok=True)  # Make the folder

    infoobject.songs = songlistin(soup)

    # Initialize the artist's value in the success dict as a dict

    success = {}
    success[infoobject.artist] = {}
    success[infoobject.artist][infoobject.album] = downloadlistofsongs(infoobject)

    # TODO Save album or add it to artist in history.json

    return infoobject



def downloadlistofsongs(infoobject):
    """Send pytube YouTube objects to download song. Return formatted dict of success songs"""
    successfulsongs = []
    infoobject.songcount = 0
    infoobject.totalcount = len(infoobject.songs)
    # mega Codeblock to download array's songs
    # Use album name + song name + "song" in YouTube search

    for songname in infoobject.songs:
        infoobject.cursong = songname
        print('\t\tDownloading - ' + songname)

        res = Search(infoobject.album + ' ' + infoobject.artist + ' song ' + songname).results
        loop = len(res)
        songlen = infoobject.songs[songname]
        if songlen == 0:
            print('\r\t\tNo song length found. Result may be inaccurate.')

        '''
        Codeblock that doesnt work, pytube get_next_results() raises indexerror
        # loop to check at least 100 videos, get_next_results doesnt pull consistent amount of videos
        while loop < 100:
            res.get_next_results()
            loop = len(res.results)            
        '''

        videos = loop

        for video in res:  # Go through videos pulled
            mismatchbool = False
            print('\r\t\tAttempting video ' + str(videos - loop + 1) + '/' + str(videos), end='\r', flush=True)
            loop -= 1
            try:
                videoname = video.title.split()

            except Exception as e:
                print(e)
                continue  # tryexcept for livestreams
            for i in range(len(videoname)):
                videoname[i] = videoname[i].lower()
            # Range is 95% to 110% of the song length
            vidlen = video.length

            # Filter for video codeblock
            if vidlen not in range(int(songlen * .95), int(songlen * 1.25)) and songlen != 0:
                mismatchbool = True
                continue

            # TODO Improve this filter further by somehow compacting into a single regex, with the same restrictions
            for word in infoobject.cursong.split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break
            for word in infoobject.album.split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break
            for word in infoobject.artist.split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break

            if not mismatchbool: break

        # check, catches if no videos in first results are
        if loop == 0:
            print('Warning: No result found within parameters - ' + songname)  # let user know about this
            continue  # move onto next songname in this case

        print('\r\t\tDownloading...', end="\r", flush=True)

        # cleanname is directory of mp4
        infoobject.songcount += 1  # increment songcount once song is found, before downloading it

        if songname in infoobject.songs:
            print('\r\t\tSong Previously Downloaded', end="\r", flush=True)
            successfulsongs.append(songname)
        else:
            try:
                if downloadsong(video, infoobject): successfulsongs.append(songname)
            except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:  # Skip to next song if above block raises an error
                print('Warning: issue downloading from YouTube - ' + songname)
                continue

    return successfulsongs


# todo implement update
def update(jsonarray):
    """Check releases and artists for previously undownloaded songs. Call writehistory."""
    return 0


# Functions that download albums or songs, after parsing info

def downloadsong(ytobj, infoobject):
    """Download MP3 from YouTube object. Return bool based on if download was successful.
    Download as MP4 for now. Downloading the MP3 stream given causes issues when trying to edit MP3 tags."""
    video = ytobj.streams.filter(type="video").order_by("abr").desc().first()
    title = video.title
    title = writable(title)
    cleanname = os.path.abspath(os.path.join(infoobject.dirstorage, title)) + '.mp4'
    video.download(filename=cleanname)

    clip = AudioFileClip(cleanname)  # make var to point to mp4's audio
    video = cleanname  # reassign video to path to mp4
    cleanname = cleanname[:-1] + '3'  # change where cleanname points
    clip.write_audiofile(cleanname, logger=None)  # write audio to an mp3 file
    os.remove(video)  # delete old mp4

    if infoobject.album:
        tagsong(cleanname, infoobject)

    print('\r', end='', flush=True)

    return os.path.exists(cleanname)


def tagsong(target, infoobject):
    """Tag MP3 with given information."""
    tagtarget = eyed3.load(target)  # creates mp3audiofile at downloaded mp3
    tagtarget = tagtarget.tag
    tagtarget.title = infoobject.cursong
    tagtarget.artist = infoobject.artist
    tagtarget.album_artist = infoobject.artist
    tagtarget.album = infoobject.album
    tagtarget.track_num = (infoobject.songcount, infoobject.totalcount)
    if infoobject.art != 'fail':  # Check if coverart is actually valid
        coverart = infoobject.art.url

        filename = os.path.join(infoobject.dirstorage, infoobject.album + ".jpeg")
        r = requests.get(coverart, stream=True)
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        with open(filename, "rb") as f:
            tagtarget.images.set(3, f.read(), "image/jpeg")
        infoobject.art = "fail"

        os.remove(filename)

    tagtarget.save(target)


# Helper functions,

def writable(rewrite):
    """Return given string, after removing all characters that would cause errors."""
    pattern = r'[:<>\*\?\\\/|\"]'
    rewrite = re.sub(pattern, "", rewrite)
    return rewrite.strip()


def songlistin(releasesoup):
    """Parse info from release page, return dict of songs and songlengths."""
    result = {}
    # find table with class, tbody inside

    # regex for tracklist_[5 alphnumchars]
    regexthing = r"tracklist_\w{5}"
    table = releasesoup.find("table", {"class": re.compile(regexthing)})
    table = table.find("tbody").find_all('tr', {})  # find table with songs
    for tr in table:
        # only consider tr if they have no class/ if they have data-track-position
        if tr.has_attr("data-track-position"):
            # find tds (columns) inside tr
            tds = tr.find_all('td')

            # 3rd tds is the song name
            name = tds[2].find("span").text

            # TODO make exception for update() with songs with 0 songlen
            try:
                # 4th tds is the song length
                length = parsetime(tds[3].text)
            except IndexError:
                length = 0

            result[name] = length

    return result


def checkhistory():
    """Write history.json if it doesn't exist yet. Return the json file opened."""
    historydir = "history.json"

    if not os.path.exists(historydir):
        with open(historydir, 'w') as f:
            json.dump({}, f)

    return historydir


# TODO implement writehistory
def writehistory(infoobj):
    """Assume:
        Infoobj is an Information object with information on new songs that have been downloaded.
    Update values in history json with given values."""
    f = open(infoobj.histstorage, 'r+')
    newhist = infoobj.songs

    try:
        #oldhist = readhistory(f)
        #oldhist = oldhist[infoobj.artist]
        oldhist = {"Made up": 100}
    except JSONDecodeError:
        pass



    newhist.update(oldhist)
    result = {infoobj.artist : newhist}


    print(json.dumps(oldhist))
    print(json.dumps(newhist))
    print(json.dumps(result))
    # write the above to the json in layered dict with information given



# TODO implement readhistory
def readhistory(file):
    """Return history.json results as a dict."""
    result = {}

    return result
