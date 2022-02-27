# import os
# import sys
from json import JSONDecodeError
import eyed3
import shutil
import urllib
import requests
from pytube import YouTube
from pytube import Search
# from useragent import UserAgent
from bs4 import BeautifulSoup
from moviepy.editor import *

# Global Variables
# ua = UserAgent()
headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) '
                          'AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13')}


# Simple menu to choose between options
def optionSelect():
    option = input('''
    Welcome to Clockknight's Album Downloader. Please choose from an option below by entering the option number:

    1) Cache Mode
    Provide a .txt file with links to album's google result pages, seperated by lines.

    2) Search Mode (Artist)
    Search for an artist's discography. Results will be stored in the 

    3) Search Mode (Album)
    Search for an album. Recommended for albums with generic artist like "Various".
    
    9) Settings
    Change the settings of the script.

    0) Exit

    ''')

    match option:
        case '1':
            cacheMode()
        case '2':
            searchMode(0)
        case '3':
            searchMode(1)
        case '9':
            print("Not implemented yet, sorry")
        case '0':
            sys.exit()
        case _:
            print('Invalid option selected. Please try again.\n\n')

    # TODO make this recursive when code's done  optionSelect() # Calls function again


def cacheMode():
    fileDir = ''
    resultArray = []

    # Find text file with links to google searches of albums' songs
    fileDir = input(
        'Please enter the directory of the text file that has the links to appropriate files separated by newlines.\n')

    # Use readlines to seperate out the links of albums
    file = open(fileDir, 'r')
    resultArray = file.readlines()
    # Run downloadAlbum
    # for item in resultArray:

    # TODO: make conditional to check json if it's artist or album
    downloadalbum(resultArray)


def searchMode(mode):
    # resultCount = 0
    # resultLinks = []
    temp = ''
    word = "artist"
    if mode == 1:
        word = "release"
    # Get input for a songwriter
    searchterm = input('\nPlease input the name of the ' + word + ' you want to search.\n\t')
    # searchLen = len(searchterm)
    urlterm = urllib.parse.quote_plus(searchterm)  # Makes artist string OK for URLs

    # discogs results scrape
    query = 'https://www.discogs.com/search/?q=' + urlterm + '&type=' + word
    try:
        page = requests.get(query, headers=headers)  # Use requests on the new URL
    except:
        print('Error:')

    match mode:
        case 0:
            print("artist mode not implemented, here's dmc5")
            downloadalbum('https://www.discogs.com/master/1575693-Various-Devil-May-Cry-5-Original-Soundtrack')
        case 1:
            soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
            divlist = soup.find_all('div',
                                    {"class": "card_large"})  # Creates a list from all the divs that make up the cards
            for div in divlist:  # Go through each div
                if div.find('h4').find('a')['title'] == searchterm:  # compare input to card's title
                    downloadalbum("https://discogs.com" + div.a["href"])  # Store first successful return then break
                    break


def downloadalbum(query):
    blacklist = '.\'/\\'  # String of characters that cannot be in filenames
    skippedList = []
    songnames = []
    songtracks = []
    songcount = 0
    infoList = []
    videoTitle = []
    titleDict = {}
    dirStorage = ''
    searchInput = ''
    artistIndex = 0

    #  tryexcept for passed query
    try:
        page = requests.get(query, headers=headers)  # Use requests on the new URL
    except:
        print('Error:')
        return

    soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it

    albumname = soup.find('h1', {"class", "title_1q3xW"})  # grabs artist and album
    artistname = albumname.find('a').text  # separate artist
    albumname = albumname.text[len(artistname) + 3:]

    #  TODO get album art
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the a tag of the cover preview
    try:
        coverart = requests.get(coverart.find('a')['href'])
    except:
        print('Warning: Problem getting album art - ' + albumname)

    # find table with class
    # find tbody inside
    table = soup.find('table', {"class": "tracklist_3QGRS"}).find("tbody").find_all('tr')
    for tr in table:
        tds = tr.find_all('td')
        songtracks.append(tds[0].text)  # note 1st td as songtrack
        songnames.append(tds[2].text)  # note 3rd td - span as song title
        songcount += 1  # increment songcount var

    # Preparing directory to download song
    dirstorage = artistname + ' - ' + albumname
    os.makedirs(dirstorage, exist_ok=True)  # Make the folder
    print('Creating folder:' + dirstorage)

    #
    # Codeblock to download array's songs
    #  TODO download each song in the array
    # Use album name + song name + "song" in youtube search
    songcount = 0
    for songname in songnames:
        page = ('https://www.google.com/search?q=' + urllib.parse.quote_plus(albumname) + '+song+'
                + urllib.parse.quote_plus(songname) + '&tbm=vid')

        try:
            page = requests.get(page, headers=headers)  # Use requests on the new URL
        except:
            print("Error: search for song on yt didn't work - " + songname)
            continue

        search = Search(albumname + ' song ' + songname)
        results = search.results
        for video in results:
            # TODO make it so the code compares songname to a regex the regex of the video title
            # video title can be found with search.results[0].title
            # Just assume it's the first video, should break
            if True:
                break

        # TODO Code keeps breaking when trying to download
        scrubname = songname
        for char in blacklist:
            scrubname = scrubname.replace(char, '')

        scrubname = os.path.join('.\\', scrubname + '.mp3')
        try:
            songcount += 1
            video.streams.filter(only_audio=True).order_by("abr").first().download(filename=scrubname)

        except JSONDecodeError:
            print('Warning: issue downloading song - ' + songname)
            skippedList.append(dirstorage + songname)
            continue

        tagtarget = eyed3.load(scrubname)
        tagtarget.tag.title = songname
        tagtarget.tag.artist = artistname
        tagtarget.tag.album = albumname
        tagtarget.tag.album_artist = artistname
        tagtarget.tag.track_num = songtracks[songcount]
        # TODO Implement adding album art
        tagtarget.tag.save()

    # Move all mp3s in the current working directory to the album folder
    for file in os.listdir('.\\'):
        if file[-4:] == '.mp3':
            shutil.move('.\\' + file, '.\\' + dirstorage + '\\' + file)

    #  TODO save song as a json in history.txt


'''
useful code snippet for checking results

                # LEVEL: Processing results for each song
                for a in aList:
                    if a['href'][:29] == 'https://www.youtube.com/watch':
                        matchIndex = 0
                        titleDict = {}

                        # Check title for matching song title
                        try:
                            # Beautiful soup the page, to check the title of the video
                            page = requests.get(a['href'], headers=headers)
                            soup = BeautifulSoup(page.text, "html.parser")
                            nameTag = soup.find('meta', {'name': 'title'})

                        except:
                            print(
                                'Failure to successfully get HTML info for page containing possible youtube results for current song!\nShutting down...')

                        videoTitle = nameTag['content']  # store the title of the video in this variable

                        songNameList = songName.split()  # Make an array of words from the song title for later

                        # Add each word in the video title to a dictionary
                        for word in videoTitle.split():
                            titleDict[word] = True

                        # Compare words in the song title to words in the dictionary. All words should be present, otherwise don't download the video.
                        for word in songNameList:
                            if word in titleDict:
                                matchIndex += 1

                        # If everything checks out, download the video then break from the loop, moving onto the next song
                        if matchIndex == len(songNameList):
                            print(
                                'Saved as: ' + songName)  # Print the title of the video for the user to know what files to look for.
                            temp = a['href']

            
'''




# Returns path to mp3 file

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


optionSelect()
