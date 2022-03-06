import time
from json import JSONDecodeError
import eyed3
import urllib
import requests
from urllib import request
from pytube import Search
from bs4 import BeautifulSoup
from moviepy.editor import *
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

''' Defining headers for user agent
headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) '
                          'AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13')}
'''


# Text based menu to choose between options
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
            searchinput(0)
        case '3':
            searchinput(1)
        case '9':
            print("Not implemented yet, sorry")
        case '0':
            sys.exit()
        case _:
            print('Invalid option selected. Please try again.\n\n')

    optionSelect()  # Calls function again


def cacheMode():
    # Find text file with links to google searches of albums' songs
    fileDir = input(
        'Please enter the directory of the text file that has the links to appropriate files separated by newlines.\n')

    # Use readlines to seperate out the links of albums
    resultArray = open(fileDir, 'r').readlines()
    # Run downloadAlbum
    # for item in resultArray:

    # TODO: make conditional to check json if it's artist or album
    downloadalbum(resultArray)


def searchinput(mode):
    word = "artist"
    if mode == 1:
        word = "release"
    # Get input for a songwriter
    searchterm = input('\nPlease input the name of the ' + word + ' you want to search.\n\t')
    searchprocess(word, searchterm)


def searchprocess(word, searchterm):
    urlterm = urllib.parse.quote_plus(searchterm)  # Makes artist string OK for URLs
    query = 'https://www.discogs.com/search/?q=' + urlterm + '&type=' + word

    try:
        page = requests.get(query)  # Use requests on the new URL
    except:
        print('Error:')

    match word:
        case 'artist':
            print("artist mode not implemented, here's dmc5")
            downloadalbum('https://www.discogs.com/master/1575693-Various-Devil-May-Cry-5-Original-Soundtrack')
        case 'release':
            soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
            divlist = soup.find_all('div',
                                    {"class": "card_large"})  # Creates a list from all the divs that make up the cards
            for div in divlist:  # Go through each div
                if div.find('h4').find('a')['title'] == searchterm:  # compare input to card's title
                    downloadalbum("https://discogs.com" + div.a["href"])  # Store first successful return then break
                    break


def downloadalbum(query):
    blacklist = '.\'/\\\"'  # String of characters that cannot be in filenames
    skippedList = []
    blacklistwords = ['Original', 'Soundtrack']
    songnames = []
    songcount = 0

    #  tryexcept for passed query
    try:
        page = requests.get(query)  # Use requests on the new URL
    except:
        print('Error:')
        return

    soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it

    albumname = soup.find('h1', {"class", "title_1q3xW"})  # grabs artist and album
    artistname = albumname.find('a').text  # separate artist
    albumname = albumname.text[len(artistname) + 3:]

    print('\tDownloading - ' + albumname)
    #  TODO get album art
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the <a> tag of the cover preview
    try:
        coverart = requests.get(coverart.find('a')['href'])
    except:
        print('Warning: Problem getting album art - ' + albumname)

    # find table with class, tbody inside
    table = soup.find('table', {"class": "tracklist_3QGRS"}).find("tbody").find_all('tr')
    for tr in table:
        tds = tr.find_all('td')
        songnames.append(tds[2].text)  # note 3rd td - span as song title

    # Preparing directory to download song
    dirstorage = artistname + ' - ' + albumname
    os.makedirs(dirstorage, exist_ok=True)  # Make the folder
    print('Creating folder:' + dirstorage)

    # Codeblock to download array's songs
    # Use album name + song name + "song" in youtube search
    for songname in songnames:
        print('\t\tDownloading - ' + songname)

        results = Search(albumname + ' song ' + songname).results
        loop = len(results)  # variable to track how many videos are past
        check = False

        for video in results:
            loop -= 1
            if video.length < 15 * 60:
                check = True
                break

        # Extra check, just in case none of the results on the first results gotten are good
        if not check and loop == 0:
            # TODO make it so code tries the loop again with results.nextresults (sic)
            print('Warning: No result found within parameters - ' + songname)
            skippedList.append(songname)
            continue  # move onto next songname in this case

        # TODO Code keeps breaking when trying to download
        cleanname = songname
        for char in blacklist:
            cleanname = cleanname.replace(char, '')

        cleanname = os.path.abspath(os.path.join(dirstorage, cleanname + '.mp4'))
        songcount += 1
        try:
            # Block is heavy in terms of process time, but only way to write downloaded youtube videos into taggable
            # mp3 files
            # video becomes youtube Object
            video = video.streams.filter(mime_type="audio/mp4").order_by("abr").desc().first()
            video.download(filename=cleanname)
            while not os.path.exists(cleanname):
                time.sleep(1)  # Wait until mp4 is downloaded
            clip = AudioFileClip(cleanname)
            video = cleanname  # reassign video to path to mp4
            cleanname = cleanname[:-1] + '3'
            clip.write_audiofile(cleanname)

            os.remove(video)

        except:
            print('Warning: issue downloading from YouTube - ' + songname)
            skippedList.append(songname)
            continue

        # TODO Implement adding album art to the eyed3 object

        tagtarget = eyed3.load(cleanname)  # creates mp3audiofile at downloaded mp3
        tagtarget = tagtarget.tag
        tagtarget.title = songname
        tagtarget.artist = artistname
        tagtarget.album_artist = artistname
        tagtarget.album = albumname
        # TODO remove hardcoded url
        coverart = 'https://upload.wikimedia.org/wikipedia/en/c/cb/Devil_May_Cry_5.jpg'
        coverart = urllib.request.urlopen(coverart)
        coverart = coverart.read()
        tagtarget.images.set(3, coverart, "image/jpeg")
        tagtarget.track_num = (songcount, len(songnames))
        tagtarget.save(cleanname)

        # TODO Save album or add it to artist in history.txt


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

# TODO update the code so the filter below works

'''Below is a currently unused filter. It only accepted videos if they had every word in the video title
videoname = video.title.split()

for i in range(0, len(videoname)):
    videoname[i] = videoname[i].lower()

for word in albumname.split():  # This should iterate through each word in the name of the album
    # Check if word exists. Also check if word is long enough
    word = word.lower()
    if word not in videoname and len(word) > 3:
        check = False
        break

if not check: continue

for word in songname.split():  # this check works the same as above, just for the song name
    word = word.lower()
    if word not in videoname:
        check = False
        break  # No point in checking the rest of the words

if check: break  # If a video gets past all the filters, then it moves on'''


# def downloadsong(songname):


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
