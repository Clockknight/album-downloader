from json import JSONDecodeError
import eyed3
import urllib
import requests
import shutil
import pytube
from pytube import YouTube, Search
from bs4 import BeautifulSoup
from moviepy.editor import *
from moviepy.audio.fx.all import *
from classes import *
import json
import re
import os

# TODO Fix the console printing out part of the artist's name when downloading GG OST
# TODO Fix other people being included into history when some releases have the current artist as a side artist
# TODO Include album #/# when printing "downloading album" message
# TODO include "artist (###)" in perfect match results in searchinput()
"""
First pass, look for each word in the release name, song name in the title, artist name in title and channel name
Second pass, also look through the videos' descriptions when looking for words in title, release name, artist name
"""


def optionselect():
    """Text menu for user to choose option"""
    option = input('''
Welcome to Clockknight's Album Downloader. Please choose from an option below by entering the option number:

1) Cache Mode
Provide a .txt file with links to album's google result pages, seperated by lines.

2) Search Mode (Artist)
Search for an artist's discography. The artist's discography will be stored in history.json

3) Search Mode (Album)
Search for an album. Recommended for albums with generic artist like "Various".

4) Update
Will check for new releases from artists that you have used this script to look at before. 

5) Redownload
Will download each song in every release, even if it has been previously downloaded. 

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
            searchinput(0)
        case '3':
            searchinput(1)
        case '4':
            update()
        case '5':
            redownload()
        case '8':
            urlinput()
        case '9':
            update()
        case '0':
            sys.exit()
        case _:
            print('Invalid option selected. Please try again.\n\n')

    return True


# Functions that take input from user, or determine logic of usage of below functions
def cacheinput():
    """Take multiple inputs from text file, ask user if given input is artist or release."""
    cachedict = {}
    # parses each line as new input, prompts user to clarify if each line is an artist or a user
    filedir = input(
        'Please enter the directory of the text file that has the links to appropriate files separated by newlines.\n')

    # Use readlines to seperate out the links of albums
    items = open(filedir, 'r').read().splitlines()
    for item in items:
        case = -1
        while case not in range(2):
            case = int(input(
                "\nItem: "
                + item +
                """
Input 0 if this is an artist
Input 1 if it is a release.
"""))

        cachedict[item] = case
    # Create dict based on items, and responses given by user

    # for item in resultArray:
    # ask user if its artist or album
    # store information in related array

    # Wait until all cache strings are processed before downloading all at once
    for key in cachedict:
        searchinput(cachedict[key], key)


def urlinput(url=None):
    """Download given YouTube URL as MP3."""
    infoobject = Information().urlsetup()
    os.makedirs(infoobject.targetstorage, exist_ok=True)  # Make the folder
    if url is None:
        url = input('\nPlease input the url of the video you want to download.\n\t')

    try:
        # Declare ytobj now to declare infoobject.art as the youtube thumbnail
        ytobj = YouTube(url)
        infoobject.art = ytobj.thumbnail_url
        downloadsong(ytobj, infoobject)
    except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:
        input("Invalid URL. Press Enter to return to the main menu.")


def searchinput(mode, searchterm=None):
    """Get user input for release or artist to search, then search it."""
    word = "artist"
    if mode == 1:
        word = "release"

    # Get input for artist/album name when no term is passed
    if searchterm is None:
        searchterm = input('\nPlease input the name of the ' + word + ' you want to search for.\n\t')

    searchprocess(word, searchterm)  # call helper function


def update():
    """Check releases and artists for previously undownloaded songs. Call writehistory."""
    infoobject = Information()

    history = readhistory(infoobject)
    for artist in history:
        searchprocess("artist", artist)


def redownload():
    # check historyjson
    history = readhistory(Information())

    # write each artist's history as {}
    for artist in history:
        history[artist] = {}
    writehistory(Information(), history)
    # then update
    update()


# Functions to parse information


def searchprocess(word, searchterm):
    """Parse relevant information and call to appropriate function."""
    result = []
    matches = []
    searchterm = searchterm.lower()
    urlterm = urllib.parse.quote_plus(searchterm)  # Makes artist string OK for URLs
    query = 'https://www.discogs.com/search/?q=' + urlterm + '&type=' + word  # makes url to search for results
    page = requests.get(query)

    # Codeblock to try and find albums based on mode provided
    soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it

    # Creates a list from all the divs that make up the cards
    elems = soup.find_all('li', {"role": "listitem"})

    # Go through each div, each one has a release/artist with a link out
    for e in elems:
        result.append(e.find('div', {"class": "card-release-title"}).find('a'))
        title = result[-1]['title'].lower()

        # If looking for artist, it takes first perfect match and escapes
        if title == searchterm and word == 'artist':  # compare input to card's title
            matches.append(result[-1])
            result.pop(-1)

    i = getuseroption(matches)

    if i:
        result = matches[i - 1]
        # goes here if useroption returns 0
    if isinstance(result, list):
        i = getuseroption(result)
        if i:
            result = result[i - 1]

        # print out the stuff and ask user for correct

    if word == 'release':
        processrelease("https://discogs.com" + result["href"])
    else:
        # Only artist mode has multipage support (Not an issue yet?)
        parseartist("https://discogs.com" + result["href"] + "?page=")


def parseartist(query):
    """Parse artist, calling parseartistpage for each page. Return formatted list of songs downloaded."""
    # TODO include method to get releases the artist is only credited in
    index = 1

    while True:
        # store array of releases to download
        try:
            releases = parseartistpage(query + str(index))
        except AttributeError as e:
            print(e)
            break

        # if nothing is returned from above, break out (query for parseartistpage was an empty page)
        if not releases:
            break
        # Process every release found
        for release in releases:
            processrelease(release)
        # go to next page of artist
        index += 1


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
    # TODO Check if multiple versions from different artists exist, get one with most songs
    infoobject = Information()
    #  tryexcept for passed query
    try:
        page = requests.get(query)  # Use requests on the new URL
        soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
    except:
        print('Error: failure processing album. Link provided - ' + query)
        return

    name = soup.find('h1', {"class", "title_1q3xW"})  # grabs artist and album
    artistname = name.find('a').text
    infoobject.setartist(artistname)  # separate artist
    infoobject.album = name.text[len(artistname) + 3:]  # grab album by removing enough characters from above var

    print('\n\tDownloading Album - ' + infoobject.album)
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the <a> tag of the cover preview
    try:
        infoobject.art = requests.get("https://discogs.com" + coverart.find('a')['href'])
    except:
        # Let the user know the album art isn't available
        print('\t\tMissed Tag: Problem getting album art - ' + infoobject.album)
        infoobject.art = 'fail'  # set it to fail for mp3 tag check

    # Preparing directory to download song
    # create folder for artist, and subfolder for release
    infoobject.targetstorage = os.path.join("Downloads", writable(infoobject.artist), writable(infoobject.album))
    os.makedirs(infoobject.targetstorage, exist_ok=True)  # Make the folder

    infoobject.songs = songlistin(soup)
    infoobject.history = readhistory(infoobject)
    writehistory(infoobject)
    infoobject = downloadlistofsongs(infoobject)
    # Call to write history to UPDATE with the songs that have been downloaded.
    writehistory(infoobject)


# Functions that download albums or songs, after parsing info

def downloadlistofsongs(infoobject):
    """Send pytube YouTube objects to download song.
    Return formatted dict of success songs, specifically for this release."""
    infoobject.songcount = 0
    infoobject.totalcount = len(infoobject.songs)
    # mega Codeblock to download array's songs
    # Use album name + song name + "song" in YouTube search

    for songname in infoobject.songs:
        infoobject.cursong = songname
        print('\t\tDownloading - ' + songname)

        res = Search(writable(infoobject.album + ' ' + infoobject.artist + ' song ' + songname))
        res.results
        loop = len(res.results)
        # loop to check at least 100 videos, get_next_results doesnt pull consistent amount of videos
        while loop < 100:
            res.get_next_results()
            loop = len(res.results)
        res= res.results

        songlen = infoobject.songs[songname]
        if songlen == 0:
            print('\r\t\tNo song length found. Result may be inaccurate.')


        # Nested if checks to see if artist, album, and song are all used
        if infoobject.artist in infoobject.history:
            temp = infoobject.history[infoobject.artist]
            if infoobject.album in temp:
                temp = temp[infoobject.album]
                if songname in temp:
                    print('\r\t\tSong Previously Downloaded, Skipping...', flush=True)
                    continue

        videos = loop

        for video in res:  # Go through videos pulled
            mismatchbool = False
            print('\r\t\tAttempting video ' + str(videos - loop + 1) + '/' + str(videos), end='\r', flush=True)
            loop -= 1
            # Range is 85% to 110% of the song length
            vidlen = video.length

            # Filter for video codeblock
            if vidlen not in range(int(songlen * .85), int(songlen * 1.25)) and songlen != 0:
                continue  # Try again with next video if it's out of range

            if searchresultfilter(infoobject, video):
                break

        # check, catches if no videos in first results are
        if loop == 0:
            print('\t\tFailed Download: No result found within parameters - ' + songname)  # let user know about this
            continue  # move onto next songname in this case

        print('\r\t\tDownloading...', end="\r", flush=True)

        # cleanname is directory of mp4
        infoobject.songcount += 1  # increment songcount once song is found, before downloading it

        # Add song to successful songs if downloadsong returns true
        try:
            if downloadsong(video, infoobject):
                infoobject.updatesuccess({songname: songlen})

        # Skip to next song if above block raises an error
        except pytube.exceptions.VideoUnavailable:
            print("blahblah")
            print('\t\tFailed Download: issue downloading from YouTube - ' + songname)
            continue

    return infoobject


def downloadsong(ytobj, infoobject):
    """Download MP3 from YouTube object. Return Bool based on if download was successful.
    Download as MP4 for now. Downloading the MP3 stream given causes issues when trying to edit MP3 tags."""
    try:
        video = ytobj.streams.filter(type="video")
    except KeyError:
        return False
    video = video.order_by("abr").desc().first()

    videopath = os.path.abspath(os.path.join(infoobject.targetstorage, writable(video.title))) + '.mp4'
    video.download(filename=videopath)

    clip = AudioFileClip(videopath)  # make var to point to mp4's audio
    clip.fx(afx.audio_normalize)
    audiopath = videopath[:-1] + '3'  # audiopath points to where the mp3 file will be
    clip.write_audiofile(audiopath, logger=None)  # write audio to audio path

    os.remove(videopath)  # delete old mp4

    if infoobject.isalbum:
        tagsong(audiopath, infoobject)

    print('\r', end='')

    return os.path.exists(audiopath)


def tagsong(target, infoobject):
    """Tag MP3 with given information. Also normalizes the audio of the file."""
    tagtarget = eyed3.load(target)  # creates mp3audiofile at downloaded mp3
    tagtarget = tagtarget.tag
    tagtarget.title = infoobject.cursong
    tagtarget.artist = infoobject.artist
    tagtarget.album = infoobject.album
    tagtarget.album_artist = infoobject.artist
    tagtarget.track_num = (infoobject.songcount, infoobject.totalcount)
    if infoobject.art != 'fail':  # Check if coverart is actually valid
        coverart = infoobject.art.url

        filename = os.path.join(infoobject.targetstorage, writable(infoobject.album) + ".jpg")
        r = requests.get(coverart, stream=True)
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        with open(filename, "rb") as f:
            tagtarget.images.set(3, f.read(), "image/jpg")
        infoobject.art = "fail"

        os.remove(filename)

    tagtarget.save(target)


# Helper functions

def writable(rewrite):
    """Return given string, after removing all characters that would cause errors."""
    pattern = r'[:<>\*\?\\\/|\/"]'
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

            try:
                # 4th tds is the song length
                length = parsetime(tds[3].text)
            except IndexError:
                length = 0

            result[name] = length

    return result


def checkhistory(infoobject=Information()):
    """Assume:
        User wants history file at location. Location informed by Information object.
    Write history.json if it doesn't exist yet. Return the directory to the file opened."""
    historydir = infoobject.histstorage
    if historydir is None:
        infoobject.histstorage, historydir = ".\\assets\\history.json"  # default history location

    if not os.path.exists(historydir):
        with open(historydir, 'w') as f:
            json.dump({}, f)

    return infoobject


def writehistory(infoobject, overwriteHist=None):
    """Assume:
        infoobject is an Information object with information on new songs that have been downloaded.
        History.json file exists
    Update values in history.json with given values.
    If overwriteHist is specified, overwrite history.json with it"""

    # Case where no overwrite history is provided
    histdir, newhist = infoobject.historyvar()
    totalhist = readhistory(infoobject)
    curartist = infoobject.artist
    # Check if the artist dict in history needs to be overwritten
    if curartist in totalhist:
        if len(totalhist[curartist]) == 1:
            if infoobject.album in totalhist[curartist]:
                # if the last two tests passed that means this is the first release to be processed, and this is the second writehistory call on that release
                totalhist[curartist][infoobject.album] = {}
        totalhist[curartist].update(newhist[curartist])
    else:
        totalhist.update(newhist)

    if overwriteHist is not None:
        totalhist = overwriteHist

    result = json.dumps(totalhist, sort_keys=True, indent=4)

    # write result to the file
    f = open(histdir, 'w')
    f.write(result)
    f.close()

 # TODO  Find way to cut off dead air before and after song plays
def readhistory(infoobject=Information()):
    """Return artist's results from history.json as a dict.
    If no artist is specified, return all results."""
    histdir = infoobject.histstorage
    if not os.path.exists(histdir):
        open(histdir, 'w+')
    f = open(histdir, 'r')

    try:
        result = json.load(f)
    # except for general json issue
    except JSONDecodeError:
        return {}
    return result


def parsetime(instring):
    """Convert hh:mm:ss strings into int value in seconds."""
    # TODO raise error if string is not in format of digits and colons
    timere = re.compile("\d+")
    colre = re.findall(':', instring)
    iter = len(colre)
    result = 0

    for value in re.findall(timere, instring):
        value = int(value)
        match (iter):
            # if 2nd iteration, then assume previous numbers are in seconds, convert to  minutes
            case 1:
                value *= 60

            # if 3rd iteration, then assume previous numbers are in minutes, convert to hours
            case 2:
                value *= 60

            # if 4th iteration, then assume previous numbers are in hours, convert to days
            case 3:
                value *= 24

        result += value
        iter -= 1

    return result


def getuseroption(tagarray):
    """Print out all of an array's item's, then ask user for an option."""
    # TODO Make this only print out 20 at a time and let user go back and forth
    length = len(tagarray)
    if not length or length == 1:
        return length
    option = -1
    lenran = range(1, length)
    display = ""
    for i in lenran:
        display += str(i) + ": " + tagarray[i - 1]['title'] + "\n"

    while option not in lenran:
        option = int(input(display))

    return option


def searchresultfilter(infoobject, video):
    """Given information from the infoobject, check if the video is within expectations of the song.
    """
    # TODO make multiple passes through each video when looking through a song
    '''
    Stages of filtering
    
    '''

    # retrieve
    artist_filter, album_song_filter = infoobject.filterwords()
    failwords = []

    try:
        videoname = video.title.split()
    except Exception as e:
        print(e)
        return False
    for i in range(len(videoname)):
        videoname[i] = videoname[i].lower()

    for word in infoobject.cursong.split():
        temp = False
        for vidword in videoname:
            if not temp and word.lower() in vidword:
                temp = True
                break
        # immediately return false if it can't be found in any of videoname's words
        if not temp:
            return False

    # Try to find word in title
    # if it's not in title, track it, then check description
    for word in filterwords:
        for vidword in videoname:
            if not temp and word.lower() in vidword:
                failwords.append(word)
                break

    # Only enter this loop if filterwords isn't empty
    if failwords:
        descwords = video.description.split()
        for word in failwords:
            temp = False
            for dword in descwords:
                if word in dword:
                    temp = True
                    break
            if not temp:
                return False

    # return true if code reaches here
    return True


# Used for testing
def clearhistory():
    f = open("assets/history.json", 'w')
    f.write("")
