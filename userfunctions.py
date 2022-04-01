import eyed3
import urllib
import pytube
import requests
from urllib import request
from pytube import Search
from bs4 import BeautifulSoup
from moviepy.editor import *
from pytube import YouTube
import shutil
import re


# Text based menu to choose between options
def optionselect():
    option = input('''
Welcome to Clockknight's Album Downloader. Please choose from an option below by entering the option number:

1) Cache Mode {Not Implemented}
Provide a .txt file with links to album's google result pages, seperated by lines.

2) Search Mode (Artist) {Not Implemented}
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

    optionselect()  # Calls function again


# Functions that take input from user, pass release pages onto parse functions

# TODO implement cacheinput
# needs to refer to clockknight want.txt, and then run
# parses each line as new input, prompts user to clarify if each line is an artist or a user
# if it is a url, note it and move on instead of actually asking

# Takes input to file that has multiple inputs from user
def cacheinput():
    # Find text file with links to google searches of albums' songs
    fileDir = input(
        'Please enter the directory of the text file that has the links to appropriate files separated by newlines.\n')


    # Use readlines to seperate out the links of albums
    historyarray = open(fileDir, 'r').readlines()
    # Run downloadlistofsongs
    # for item in resultArray:

    # Pass array of artist jsons to update()
    update(historyarray)


# user gives url as input, script downloads single song
def urlinput():
    dirstorage = "URL Downloads"
    infodict = {"dirstorage": dirstorage}
    os.makedirs(dirstorage, exist_ok=True)  # Make the folder
    url = input('\nPlease input the url of the video you want to download.\n\t')

    try:
        # Declare ytobj now to declare infodict[albumart] as the youtube thumbnail
        ytobj = YouTube(url)
        infodict["albumart"] = ytobj.thumbnail_url
        downloadsong(ytobj, infodict)
    except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:
        input("Invalid URL. Press Enter to return to the main menu.")
        optionselect()


# code that defines if  input is an artist or a release
def searchinput(mode, searchterm):

    word = "artist"
    if mode == 1:
        word = "release"

    # Get input for artist/album name when no term is passed
    if searchterm == "":
        searchterm = input('\nPlease input the name of the ' + word + ' you want to search for.\n\t')

    searchprocess(word, searchterm)  # call helper function


# Finds artist or release based on word and searchterm passed
def searchprocess(word, searchterm):
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
        # TODO Check if multiple versions from different artists exist
        result = div.find('h4').find('a')['title'].lower()
        if result == searchterm:  # compare input to card's title
            match word:
                case 'release':
                    parserelease("https://discogs.com" + div.a["href"])  # Store first successful return then break
                case 'artist':
                    # Fake do while loop
                    # Does
                    index = 1
                    while True:
                        # store array returned from parseartist in value
                        value = parseartist("https://discogs.com" + div.a["href"] + "?page=" + str(index))
                        # if nothing is returned, break out
                        if not value:
                            break
                        # pass each release url into parserelease to be scraped
                        for release in value:
                            parserelease(release)
                        # go to next page of artist
                        index += 1

            # stops code from trying to scrape other release/artists
            break

        # Adds name of artist to array if its not a match
        if result not in resultartiststhatarentmatching: resultartiststhatarentmatching.append(result)

    # Fail case here (this assumes first page has 0 results)


# Function finds all releases from an artist, returns array of release urls
def parseartist(query):
    results = []
    soup = requests.get(query)
    soup = BeautifulSoup(soup.text, "html.parser")

    # < table class ="cards table_responsive layout_normal" id="artist" >
    trs = soup.find("table", id="artist").find_all("tr")
    for tr in trs:
        # Every tr with an album has this attribute
        if tr.has_attr("data-group-url"):
            tr = tr.find("a")
            results.append("https://discogs.com" + tr["href"])

    return results


# Function finds information in release page and stores in infodict. Calls downloadlistofsongs
def parserelease(query):
    infodict = {}

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
    infodict['albumname'] = name.text[len(artistname) + 3:]  # grab album by removing enough characters from above var

    print('\n\tDownloading Album - ' + infodict["albumname"])
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the <a> tag of the cover preview
    try:
        infodict["coverart"] = requests.get("https://discogs.com" + coverart.find('a')['href'])
    except:
        print('Warning: Problem getting album art - ' + infodict[
            "albumname"])  # Let the user know the album art isn't available
        infodict["coverart"] = 'fail'  # set it to fail for mp3 tag check

    # Preparing directory to download song
    infodict["dirstorage"] = os.path.join(writable(infodict["artistname"]),
                                          writable(infodict["albumname"]))  # create folder for artist, and subfolder for release
    os.makedirs(infodict["dirstorage"], exist_ok=True)  # Make the folder

    infodict["songs"] = songlistin(soup)

    skippedlist = downloadlistofsongs(infodict)
    # TODO make this append skippedlist to skipped songs on the json


# Function that gets Youtube Objects ready to send to downloadsong
def downloadlistofsongs(infodict):
    skippedList = []
    infodict["songcount"] = 0
    infodict["totalcount"] = len(infodict["songs"])
    # mega Codeblock to download array's songs
    # Use album name + song name + "song" in youtube search

    for songname in infodict["songs"]:
        infodict["cursongname"] = songname
        print('\t\tDownloading - ' + songname)

        res = Search(infodict["albumname"] + ' song ' + songname).results
        loop = len(res)
        check = False
        # Check at least 100 videos
        '''
        Codeblock that doesnt work, pytube get_next_results() raises indexerror
        while True:
            res.get_next_results()
            loop = len(res.results)

            if loop >= 100: break
        '''

        for video in res:  # Go through videos pulled
            loop -= 1
            videoname = video.streams[0].title.split()
            # Range is 95% to 110% of the song length
            vidlen = video.length

            songlen = parsetime(infodict["songs"][songname])

            if songlen not in range(vidlen * .95, vidlen * 1.1):
                check = True
                break

            ''' 
            Better filter WIP:
            
            
            '''
            for word in infodict["cursongname"].split():
                if word not in videoname:
                    check = True
                    break
            for word in infodict["albumname"].split():
                if word not in videoname:
                    check = True
                    break
            for word in infodict["artistname"].split():
                if word not in videoname:
                    check = True
                    break

        # check, catches if no videos in first results are
        if not check and loop == 0:
            print('Warning: No result found within parameters - ' + songname)  # let user know about this
            skippedList.append(songname)  # put it on the skipped songs
            continue  # move onto next songname in this case

        # if check to see if loop is working

        cleanname = writable(songname)  # remove chars that will mess up processing below

        # cleanname is directory of mp4
        cleanname = os.path.abspath(os.path.join(infodict["dirstorage"], cleanname + '.mp4'))
        infodict["songcount"] += 1  # increment songcount once song is found, before downloading it

        try:
            if not downloadsong(video, infodict):
                skippedList.append(songname)
        except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:  # Skip to next song if above block raises an error
            print('Warning: issue downloading from YouTube - ' + songname)
            skippedList.append(songname)
            continue

        # TODO Save album or add it to artist in history.json

    return skippedList


# Function to download any releases that are on the artist's discog page but not in any of the jsons in jsonarray
def update(jsonarray):
    return 0


# Functions that download albums or songs, after parsing info

# Function that downloads song, calls tagsong if the mp3 is part of an album. Returns bool based on if the mp3 file exists.
def downloadsong(ytobj, infodict):
    video = ytobj.streams.filter(type="video").order_by("abr").desc().first()
    title = video.title
    title = writable(title)
    cleanname = os.path.abspath(os.path.join(infodict["dirstorage"], title)) + '.mp4'
    video.download(filename=cleanname)

    clip = AudioFileClip(cleanname)  # make var to point to mp4's audio
    video = cleanname  # reassign video to path to mp4
    cleanname = cleanname[:-1] + '3'  # change where cleanname points
    clip.write_audiofile(cleanname, logger=None)  # write audio to an mp3 file
    os.remove(video)  # delete old mp4

    if "albumname" in infodict:
        tagsong(cleanname, infodict)

    return os.path.exists(cleanname)


# Song tags mp3 with info from infodict
def tagsong(target, infodict):
    tagtarget = eyed3.load(target)  # creates mp3audiofile at downloaded mp3
    tagtarget = tagtarget.tag
    tagtarget.title = infodict["cursongname"]
    tagtarget.artist = infodict["artistname"]
    tagtarget.album_artist = infodict["artistname"]
    tagtarget.album = infodict["albumname"]
    tagtarget.track_num = (infodict["songcount"], infodict["totalcount"])
    if infodict["coverart"] != 'fail':  # Check if coverart is actually valid
        coverart = infodict["coverart"].url

        filename = os.path.join(infodict["dirstorage"], infodict["albumname"] + ".jpeg")
        r = requests.get(coverart, stream=True)
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        with open(filename, "rb") as f:
            tagtarget.images.set(3, f.read(), "image/jpeg")
        infodict["coverart"] = "fail"

    tagtarget.save(target)


# Helper functions

# Function returns rewrite but removing characters not allowed in Windows file names
def writable(rewrite):
    pattern = r'[:<>\*\?\\\/|\"]'
    rewrite = re.sub(pattern, "", rewrite)
    return rewrite



# Function parses information from the release page on discogs, returns array of songnames
def songlistin(releasesoup):
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

            # 4th tds is the song length
            length = tds[3].text

            result[name] = length

    return result

# Function parses time formats from discogs
def parsetime(instring):
    timere = re.search('\d{1,2}', instring)
    result = 0



    for value in timere:
        result += value

    return int(result)