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
from pydub import AudioSegment, effects
import json
import re
import os


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
            searchinput(0)
        case '3':
            searchinput(1)
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
    cachedict = {}
    # parses each line as new input, prompts user to clarify if each line is an artist or a user
    filedir = input(
        'Please enter the directory of the text file that has the links to appropriate files separated by newlines.\n')

    # Use readlines to seperate out the links of albums
    items = open(filedir, 'r').readlines()
    for item in items:
        case = -1
        while case not in range(2):
            case = int(input(
                "\nItem: "
                + item +
                """Input 0 if this is an artist
Input 1 if it is a release. """))

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
    infoobject = Information()
    infoobject.init()
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


# Functions to parse information


def searchprocess(word, searchterm):
    """Parse relevant information and call to appropriate function."""
    result = []
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
        result.append(div.find('h4').find('a')['title'].lower())

        # If looking for artist, it takes first perfect match and escapes
        if result[-1] == searchterm and word == 'artist':  # compare input to card's title
            result = result[-1]
            break

    if word == 'release':
        success = processrelease("https://discogs.com" + result.a["href"])
    else:
        # Only artist mode has multipage support (Not an issue yet?)
        success = parseartist("https://discogs.com" + result.a["href"] + "?page=")

    # After above search runs, write to the history json then break
    # Both return a success object
    writehistory(success)

    # Should print out unique results scraped, and give user chance to correct input


def parseartist(query):
    """Parse artist, calling parseartistpage for each page. Return formatted list of songs downloaded."""
    # TODO include method to get releases the artist is only credited in
    index = 1
    infoobj = Information()

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
            infoobj.update(processrelease(release))
        # go to next page of artist
        index += 1

    return infoobj


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


def processrelease(query, infoobject=None):
    """Parse information for release and send to downloadlistofsongs. Return formatted dict of success songs."""
    # TODO Check if multiple versions from different artists exist, get one with most songs
    if infoobject is None:
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
    infoobject.artist = artistname  # separate artist
    infoobject.release = name.text[len(artistname) + 3:]  # grab album by removing enough characters from above var

    print('\n\tDownloading Album - ' + infoobject.release)
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the <a> tag of the cover preview
    try:
        infoobject.art = requests.get("https://discogs.com" + coverart.find('a')['href'])
    except:
        # Let the user know the album art isn't available
        print('\t\tWarning: Problem getting album art - ' + infoobject.release)
        infoobject.art = 'fail'  # set it to fail for mp3 tag check

    # Preparing directory to download song
    # create folder for artist, and subfolder for release
    infoobject.targetstorage = os.path.join(writable(infoobject.artist), writable(infoobject.release))
    os.makedirs(infoobject.targetstorage, exist_ok=True)  # Make the folder

    infoobject.songs = songlistin(soup)
    infoobject.history = readhistory(infoobject.histstorage, infoobject.artist)
    infoobject.success = {infoobject.release: downloadlistofsongs(infoobject)}

    # TODO Save album or add it to artist in history.json

    return infoobject


def downloadlistofsongs(infoobject):
    """Send pytube YouTube objects to download song.
    Return formatted dict of success songs, specifically for this release."""
    successfulsongs = {}
    infoobject.songcount = 0
    infoobject.totalcount = len(infoobject.songs)
    # mega Codeblock to download array's songs
    # Use album name + song name + "song" in YouTube search

    for songname in infoobject.songs:
        infoobject.cursong = songname
        print('\t\tDownloading - ' + songname)

        res = Search(infoobject.release + ' ' + infoobject.artist + ' song ' + songname).results
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
                break

            # TODO Improve this filter further by somehow compacting into a single regex, with the same restrictions
            for word in infoobject.cursong.split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break
            for word in infoobject.release.split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break
            for word in infoobject.artist.split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break

            if not mismatchbool:
                break

        # check, catches if no videos in first results are
        if loop == 0:
            print('Warning: No result found within parameters - ' + songname)  # let user know about this
            continue  # move onto next songname in this case

        print('\r\t\tDownloading...', end="\r", flush=True)

        # cleanname is directory of mp4
        infoobject.songcount += 1  # increment songcount once song is found, before downloading it

        if songname in infoobject.history:
            print('\r\t\tSong Previously Downloaded')
        else:
            # Add song to successful songs if downloadsong returns true
            try:
                if downloadsong(video, infoobject):
                    successfulsongs.update({songname: songlen})

            # Skip to next song if above block raises an error
            except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:
                print('Warning: issue downloading from YouTube - ' + songname)
                continue

    return successfulsongs


def update():
    """Check releases and artists for previously undownloaded songs. Call writehistory."""
    infoobj = Information()

    history = readhistory(infoobj.histstorage)
    for artist in history:
        searchprocess("artist", artist)


# Functions that download albums or songs, after parsing info

def downloadsong(ytobj, infoobject):
    """Download MP3 from YouTube object. Return Bool based on if download was successful.
    Download as MP4 for now. Downloading the MP3 stream given causes issues when trying to edit MP3 tags."""
    video = ytobj.streams.filter(type="video").order_by("abr").desc().first()
    title = video.title
    title = writable(title)
    cleanname = os.path.abspath(os.path.join(infoobject.targetstorage, title)) + '.mp4'
    video.download(filename=cleanname)

    clip = AudioFileClip(cleanname)  # make var to point to mp4's audio
    video = cleanname  # reassign video to path to mp4
    cleanname = cleanname[:-1] + '3'  # change where cleanname points
    clip.write_audiofile(cleanname, logger=None)  # write audio to an mp3 file
    os.remove(video)  # delete old mp4

    if infoobject.release:
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
    tagtarget.release = infoobject.release
    tagtarget.track_num = (infoobject.songcount, infoobject.totalcount)
    if infoobject.art != 'fail':  # Check if coverart is actually valid
        coverart = infoobject.art.url

        filename = os.path.join(infoobject.targetstorage, infoobject.release + ".jpeg")
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


def checkhistory(historydir=None):
    """Assume:
        User wants history file at location. Location informed by Settings object.
    Write history.json if it doesn't exist yet. Return the directory to the file opened."""
    # TODO make this informed by settings object
    if historydir is None:
        historydir = "history.json"

    if not os.path.exists(historydir):
        with open(historydir, 'w') as f:
            json.dump({}, f)

    return historydir


def writehistory(infoobj):
    """Assume:
        Infoobj is an Information object with information on new songs that have been downloaded.
        History.json exists prior to now
    Update values in history json with given values."""
    artist = infoobj.artist
    release = infoobj.release
    histdir = infoobj.histstorage
    newhist = infoobj.success

    totalhist = readhistory(histdir, artist)

    # merge and format old and new lists of songs downloaded.
    if release in totalhist:
        totalhist[release].update(newhist[release])
    else:
        totalhist.update(newhist)
    result = json.dumps({infoobj.artist: totalhist}, sort_keys=True, indent=4)

    # write result to the file
    f = open(histdir, 'w')
    f.write(result)
    f.close()


def readhistory(histdir, artist=None):
    """Return artist's results from history.json as a dict.
    If no artist is specified, return all results."""
    f = open(histdir, 'r')

    try:
        result = json.load(f)
    # except for general json issue
    except JSONDecodeError:
        return result == {}
    if artist is None:
        return result
    elif artist in result:
        return result[artist]
    else:
        return {}


# Used for testing
def clearhistory():
    f = open("history.json", 'w')
    f.write("")

    test("./Ken Ashcorp")
    test("/Various")
    test("./URL Downloads")
    test("./GGRIM")
    test("./Cxxlion")

    # Hard coded folder remove values for testing purposes


def test(testdir):
    os.makedirs(testdir, exist_ok=True)
    shutil.rmtree(testdir)


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
