import eyed3
import urllib
import pytube
import requests
from urllib import request
from pytube import Search
from bs4 import BeautifulSoup
from moviepy.editor import *
from pytube import YouTube
import ssl
import re


# Text based menu to choose between options
def optionSelect():
    global infodict
    infodict = {}

    option = input('''
Welcome to Clockknight's Album Downloader. Please choose from an option below by entering the option number:

1) Cache Mode
Provide a .txt file with links to album's google result pages, seperated by lines.

2) Search Mode (Artist)
Search for an artist's discography. The artist's discography will be stored in history.json

3) Search Mode (Album)
Search for an album. Recommended for albums with generic artist like "Various".

8) URL Mode
Paste in a URL, and the program will do it's best to parse the information.

9) Settings
Change the settings of the script.

0) Exit

    ''')

    match option:
        case '1':
            cacheMode()
        case '2':
            searchinput(0)
        case '3':
            searchinput(1)
        case '8':
            urlinput()
        case '9':
            print("Not implemented yet, sorry")
        case '0':
            sys.exit()
        case _:
            print('Invalid option selected. Please try again.\n\n')

    optionSelect()  # Calls function again


# TODO implement cacheMode
# needs to refer to clockknight want.txt, and then run
# parses each line as new input, prompts user to clarify if each line is an artist or a user
# if it is a url, note it and move on instead of actually asking
def cacheMode():
    # Find text file with links to google searches of albums' songs
    fileDir = input(
        'Please enter the directory of the text file that has the links to appropriate files separated by newlines.\n')

    # Use readlines to seperate out the links of albums
    historyarray = open(fileDir, 'r').readlines()
    # Run downloadAlbum
    # for item in resultArray:

    # Pass array of artist jsons to update()
    update(historyarray)


# user gives url as input, script downloads single song
def urlinput():
    dirstorage = "URL Downloads"
    infodict["dirstorage"] = dirstorage
    os.makedirs(dirstorage, exist_ok=True)  # Make the folder

    url = input('\nPlease input the url of the video you want to download.\n\t')
    downloadsong(YouTube(url))


# code that defines if  input is an artist or a release
def searchinput(mode):
    word = "artist"
    if mode == 1:
        word = "release"
    # Get input for artist/album name
    searchterm = input('\nPlease input the name of the ' + word + ' you want to search for.\n\t')
    searchprocess(word, searchterm)  # call helper function


# Finds artist or release based on word and searchterm passed
def searchprocess(word, searchterm):
    urlterm = urllib.parse.quote_plus(searchterm)  # Makes artist string OK for URLs
    query = 'https://www.discogs.com/search/?q=' + urlterm + '&type=' + word  # makes url to search for results

    try:
        page = requests.get(query)  # Use requests on the new URL
    except:
        print('Error:')

    # Codeblock to try and find albums based on mode provided
    match word:
        case 'artist':
            print("artist mode not implemented, here's dmc5")
            parserelease('https://www.discogs.com/master/1575693-Various-Devil-May-Cry-5-Original-Soundtrack')
        case 'release':
            soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
            divlist = soup.find_all('div',
                                    {"class": "card_large"})  # Creates a list from all the divs that make up the cards
            for div in divlist:  # Go through each div
                if div.find('h4').find('a')['title'] == searchterm:  # compare input to card's title
                    parserelease("https://discogs.com" + div.a["href"])  # Store first successful return then break
                    break


def parserelease(query):
    infodict = {}
    blacklistwords = ['Original', 'Soundtrack']
    songcount = 0

    #  tryexcept for passed query
    try:
        page = requests.get(query)  # Use requests on the new URL
        soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
    except:
        print('Error: failure processing album. Link provided - ' + query)
        return

    name = soup.find('h1', {"class", "title_1q3xW"})  # grabs artist and album
    artistname = name.find('a').text
    infodict["artistname"] = artistname  # separate artist
    infodict["albumname"] = name.text[len(artistname) + 3:]  # grab album by removing enough characters from above var

    print('\tDownloading - ' + infodict["albumname"])
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the <a> tag of the cover preview
    try:
        # TODO actually implement a way to get the album art from the discogs page
        infodict["coverart"] = requests.get(coverart.find('a')['href'])
    except:
        print('Warning: Problem getting album art - ' + infodict[
            "albumname"])  # Let the user know the album art isn't available
        infodict["coverart"] = 'fail'  # set it to fail for mp3 tag check

    # Preparing directory to download song
    infodict["dirstorage"] = os.path.join(infodict["artistname"],
                                          infodict["albumname"])  # create folder for artist, and subfolder for release
    os.makedirs(infodict["dirstorage"], exist_ok=True)  # Make the folder

    skippedlist = downloadalbum(songlistin(soup))


# Takes list of words from search, returns words that should be the artist's name
def searchParse(searchTerms):
    artistIndex = 0
    confirmedString = ''

    while artistIndex == 0:
        artistIndex = input(
            'Please input how many words long the artist\'s name is. (Each word is printed above in a new line.)\n')
        if artistIndex.isnumeric():  # Check to make sure the string is made of numbers
            artistIndex = int(artistIndex)  # Convert the string into an integer
            if artistIndex <= 0 or artistIndex > len(searchTerms):  # Check if the input is within the
                print('Sorry, not a valid response. Please try again.')
                artistIndex = 0
            else:
                for i in range(0, artistIndex):
                    confirmedString += (str(searchTerms[i])) + ' '

        return confirmedString


def downloadalbum(songnames):
    coverart = infodict["coverart"]
    skippedList = []
    songcount = 0
    # mega Codeblock to download array's songs
    # Use album name + song name + "song" in youtube search
    for songname in songnames:
        print('\t\tDownloading - ' + songname)

        results = Search(infodict["albumname"] + ' song ' + songname).results
        loop = len(results)  # variable to track how many videos are past
        check = False

        for video in results:  # Go through videos pulled
            loop -= 1
            if video.length < 15 * 60:  # only filter in place is making sure the video is at least 15 min
                check = True
                break  # break out of check

        # check, catches if no videos in first results are
        if not check and loop == 0:
            # TODO make it so code tries the loop again with results.nextresults (sic)
            print('Warning: No result found within parameters - ' + songname)  # let user know about this
            skippedList.append(songname)  # put it on the skipped songs
            continue  # move onto next songname in this case

        cleanname = writable(songname)  # remove chars that will mess up processing below

        cleanname = os.path.abspath(
            os.path.join(infodict["dirstorage"], cleanname + '.mp4'))  # cleanname is directory of mp4
        songcount += 1  # increment songcount once song is found, before downloading it
        try:
            # TODO: Replace below with call to some function
            # Block is heavy in terms of process time, but only way to write downloaded youtube videos into taggables
            # if possible, a way to download a mp3 directly would be useful
            # downloadsong()
            video = video.streams.filter(mime_type="audio/mp4").order_by("abr").desc().first()
            video.download(filename=cleanname)  # download video as mp4
            clip = AudioFileClip(cleanname)  # make var to point to mp4's audio
            video = cleanname  # reassign video to path to mp4
            cleanname = cleanname[:-1] + '3'  # change where cleanname points
            clip.write_audiofile(cleanname)  # write audio to an mp3 file

            os.remove(video)  # delete old mp4

        except:  # Skip to next song if above block raises an error
            print('Warning: issue downloading from YouTube - ' + songname)
            skippedList.append(songname)
            continue

        tagtarget = eyed3.load(cleanname)  # creates mp3audiofile at downloaded mp3
        tagtarget = tagtarget.tag
        tagtarget.title = songname
        tagtarget.artist = infodict["artistname"]
        tagtarget.album_artist = infodict["artistname"]
        tagtarget.album = infodict["albumname"]
        tagtarget.track_num = (songcount, len(songnames))
        if coverart != 'fail':  # Check if coverart is actually
            coverart = urllib.request.urlopen(infodict["coverart"])
            coverart = coverart.read()
            tagtarget.images.set(3, coverart, "image/jpeg")
            coverart = "fail"

        tagtarget.save(cleanname)

        # TODO Save album or add it to artist in history.json

    return skippedList



def writable(input):
    # Function returns input but removing characters not allowed in windows file names
    pattern = r'[:<>#%&{}\*\?\\\/|]'
    input = re.sub(pattern, "", input)
    return input


def songlistin(releasesoup):
    result = []
    # find table with class, tbody inside
    # regex for tracklist_[5 alphnumchars]
    regexthing = r"tracklist_\w{5}"
    table = releasesoup.find("table", {"class": re.compile(regexthing)})
    table = table.find("tbody").find_all('tr', {})  # find table with songs
    for tr in table:
        # only consider tr if they have no class/ if they have data-track-position
        if tr.has_attr("data-track-position"):
            search = tr.find_all('td')  # find tds (columns) inside tr
            search = search[2]
            search = search.find("span")
            search = search.text
            result.append(search)  # note 3rd td - span as song title

    return result


def downloadsong(ytobj):
    try:
        video = ytobj.streams.filter(type="video").order_by("abr").desc().first()
        title = video.title
        title = writable(title)
        cleanname = os.path.abspath(os.path.join(infodict["dirstorage"], title)) + '.mp4'
        video.download(filename=cleanname)

        # TODO: Make this code block (also present in the album download function) a helper function instead
        clip = AudioFileClip(cleanname)  # make var to point to mp4's audio
        video = cleanname  # reassign video to path to mp4
        cleanname = cleanname[:-1] + '3'  # change where cleanname points
        clip.write_audiofile(cleanname)  # write audio to an mp3 file
        os.remove(video)  # delete old mp4
    except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:
        input("Invalid URL. Press Enter to return to the main menu.")
        optionSelect()
        ''' except:
        input("Unexpected error, please create an issue on https://github.com/Clockknight/album-downloader/issues.\n"
              "Press Enter to return to the main menu.")
        optionSelect()'''


# def tagsong(ytobj?):
def createfolder(dirthing):
    return 0


def update(jsonarray):
    # function to download any releases that are on the artist's discog page but not in any of the jsons in jsonarray
    return 0
