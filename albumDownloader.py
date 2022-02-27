# import os
# import sys
from json import JSONDecodeError
import eyed3
import shutil
import urllib
import requests
from pytube import YouTube
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

    #  tryexcept for passed query
    try:
        page = requests.get(query, headers=headers)  # Use requests on the new URL
    except:
        print('Error:')

    soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
    #  TODO get album art
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the a tag of the cover preview
    try:
        coverart = requests.get(coverart.find('a')['href'])
    except:
        print('Error:')


    #  TODO make song array
    #  TODO download each song in the array
    #  TODO save song as a json in history.txt
    '''

    # LEVEL: Processing google search links
    for link in givenArray:
        # Refresh variables for each link
        songNameList = []
        songList = []
        infoList = []
        videoTitle = []
        titleDict = {}
        dirStorage = ''
        searchInput = ''
        artistName = ''
        albumName = ''
        songName = ''
        songCount = 0
        artistIndex = 0

        # Process each link and grab song titles from the pages
        try:
            page = requests.get(link, headers=headers)  # Use requests on the new URL
            soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it

        except:
            print('Failure to successfully get HTML info for page containing the album\'s songs!\nSkipping Album...')

        # Get album and artist title to save as folder
        searchInput = soup.find('title')
        searchInput = searchInput.contents[0][:-22]
        # Ask user for input regarding the artist's name in the search
        infoList = searchInput.split()
        for item in infoList:
            print(item)

        # Processing search query to find album and artist names
        artistName = searchParse(infoList)
        artistName = artistName.capitalize()
        # Let user know about album info
        print('Artist name: ' + artistName)
        # Update infoList to exclude the artist name
        for word in infoList[len(artistName.split()):]:
            albumName += word.capitalize() + ' '
        print('Album name: ' + albumName + '\n')
        # Create folder based on album info
        dirStorage = artistName + ' - ' + albumName
        dirStorage = dirStorage[:-1]  # Remove whitespace at the end of the string
        os.makedirs(dirStorage, exist_ok=True)  # Make the folder
        print('Creating folder:' + dirStorage)

        divList = soup.find_all('div', {'class': 'title'})
        for div in divList:
            songList.append(div.contents[0])  # Refer to the first item of contents, since .contents returns an array

            # LEVEL: Processing entire albums
            # Process each song by appending the song title to the search
            songIndex = songCount
            for item in songList:
                songName = item
                print('\nSong name: ' + songName)
                songIndex -= 1
                # temp stores each song's google search video results
                temp = 'https://www.google.com/search?q=' + item.replace(" ", "+") + '+' + link[32:] + '&tbm=vid'
                try:
                    page = requests.get(temp, headers=headers)  # Use requests on the new URL
                    soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it

                except:
                    print(
                        'Failure to successfully get HTML info for youtube result page for current song!\nShutting down...')

                # Look for links in search results
                aList = soup.find_all('a', href=True)

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

                            scrubbedName = songName
                            for char in blacklist:
                                scrubbedName = scrubbedName.replace(char, '')

                            # TODO Add try except case for json.decoder.JSONDecodeError
                            try:
                                songCount += 1
                                YouTube(temp).streams.first().download(filename=scrubbedName)

                            except JSONDecodeError:
                                print('Song download error! Skipped song: ' + songName)
                                skippedList.append(dirStorage + songName)
                                pass

                            # Create versions of the variables with blacklisted characters removed
                            targetFile = os.path.join('.\\', scrubbedName + '.mp4')

                            # Change file into an mp3
                            targetFile = convertFile(targetFile)
                            print(targetFile)

                            tagTarget = eyed3.load(targetFile)
                            tagTarget.tag.title = songName
                            tagTarget.tag.artist = artistName
                            tagTarget.tag.album = albumName
                            tagTarget.tag.album_artist = artistName
                            tagTarget.tag.track_num = songCount
                            # TODO Implement adding album art
                            tagTarget.tag.save()

                            break  # Move onto processing next song

            # Move all mp3s in the current working directory to the album folder
            for file in os.listdir('.\\'):
                if file[-4:] == '.mp3':
                    shutil.move('.\\' + file, '.\\' + dirStorage + '\\' + file)
'''


# Converts given mp4 file into an mp3 file
def convertFile(givenFile):
    resultFile = givenFile[:-1] + '3'

    givenMp4 = VideoFileClip(givenFile)
    audioMp4 = givenMp4.audio
    audioMp4.write_audiofile(resultFile)
    givenMp4.close()
    audioMp4.close()
    os.remove(givenFile)

    return resultFile


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
