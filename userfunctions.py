import eyed3
import urllib
import pytube
import requests
import json
import shutil
import re
from pytube import Search
from pytube import YouTube
from bs4 import BeautifulSoup
from moviepy.editor import *


# Text based menu to choose between options
def optionselect():
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
    cachearray = open(fileDir, 'r').readlines()
    # Run downloadlistofsongs
    # for item in resultArray:
    # ask user if its artist or album
    # store information in related array

    # after for loop, call releaseinput() or artistinput() based on inputs given before


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
            # Run different function mode chosen
            match word:
                case 'release':
                    success = downloadrelease("https://discogs.com" + div.a["href"])
                case 'artist':
                    # Only artist mode has multipage support (Not an issue yet?)
                    success = parseartist("https://discogs.com" + div.a["href"] + "?page=")

            # After above search runs, write to the history json then break
            writejson(word, success)
            break

        # TODO Make this write to json just the artist, since no results were found
        # Adds name of artist to array if its not a match
        if result not in resultartiststhatarentmatching: resultartiststhatarentmatching.append(result)

    # TODO Make Fail case here (this assumes first page has 0 results)
    # Should print out unique results scraped, and give user chance to correct input


# function that calls parseartistpage for each page in the given artist page, returns dicts of success songs in releases
def parseartist(query):
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
            success.update(downloadrelease(release))
        # go to next page of artist
        index += 1

    return success


# Function finds all releases from a single artist's page, returns array of release urls
def parseartistpage(query):
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


# Function finds information in release page and stores in infodict. Calls downloadlistofsongs
def downloadrelease(query):
    infodict = {}
    success = {"artists": {}}

    infodict["history"] = checkhistory()

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
                                          writable(infodict[
                                                       "albumname"]))  # create folder for artist, and subfolder for release
    os.makedirs(infodict["dirstorage"], exist_ok=True)  # Make the folder

    infodict["songs"] = songlistin(soup)

    # Initialize the artist's value in the success dict as a dict
    success = success[infodict["artistname"]]
    success = {}

    success[infodict["albumname"]] = downloadlistofsongs(infodict)

    # TODO Save album or add it to artist in history.json

    return success


# Function that gets Youtube Objects ready to send to downloadsong
def downloadlistofsongs(infodict):
    successfulsongs = []
    infodict["songcount"] = 0
    infodict["totalcount"] = len(infodict["songs"])
    # mega Codeblock to download array's songs
    # Use album name + song name + "song" in youtube search

    for songname in infodict["songs"]:
        infodict["cursongname"] = songname
        print('\t\tDownloading - ' + songname)

        res = Search(infodict["albumname"] + ' song ' + songname).results
        loop = len(res)
        songlen = parsetime(infodict["songs"][songname])
        # check at least 100 videos
        '''
        Codeblock that doesnt work, pytube get_next_results() raises indexerror
        while True:
            res.get_next_results()
            loop = len(res.results)

            if loop >= 100: break
        '''

        videos = loop

        for video in res:  # Go through videos pulled
            mismatchbool = False
            print('\r\t\tAttempting video ' + str(videos - loop + 1) + '/' + str(videos), end='\r', flush=True)
            loop -= 1
            try:
                videoname = video.streams[0].title.split()
            except Exception as e:
                print(e)
                continue  # tryexcept for livestreams
            for i in range(len(videoname)):
                videoname[i] = videoname[i].lower()
            # Range is 95% to 110% of the song length
            vidlen = video.length

            # Filter for video codeblock
            if vidlen not in range(int(songlen * .95), int(songlen * 1.25)):
                mismatchbool = True
                continue

            # TODO Improve this filter further by somehow compacting into a single regex, with the same restrictions
            for word in infodict["cursongname"].split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break
            for word in infodict["albumname"].split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break
            for word in infodict["artistname"].split():
                if mismatchbool or (word.lower() not in videoname):
                    mismatchbool = True
                    break

            if not mismatchbool: break

        # check, catches if no videos in first results are
        if loop == 0:
            print('Warning: No result found within parameters - ' + songname)  # let user know about this
            continue  # move onto next songname in this case

        print('\r\t\tDownloading...', end="\n", flush=True)

        # if check to see if loop is working

        cleanname = writable(songname)  # remove chars that will mess up processing below

        # cleanname is directory of mp4
        cleanname = os.path.abspath(os.path.join(infodict["dirstorage"], cleanname + '.mp4'))
        infodict["songcount"] += 1  # increment songcount once song is found, before downloading it

        try:
            if downloadsong(video, infodict): successfulsongs.append(songname)
        except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:  # Skip to next song if above block raises an error
            print('Warning: issue downloading from YouTube - ' + songname)
            continue

    return successfulsongs


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
    # TODO raise error if string is not in format of digits and colons
    timere = re.compile('\d+')
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


# Function writes cache.json if it doesnt exist yet
def checkhistory():
    historydir = "history.json"

    if not os.path.exists(historydir):
        with open(historydir, 'w') as f:
            json.dump({}, f)

    return open(historydir)


def writejson(case, valuearray):
    # assume the following:
    # case is "artist" or "release"
    # slot 0 is json location
    # slot 1 is name of artist
    # slot 2 is dict of releases
        # keys are release titles
        # values are successful songs in those releases

    # write the above to the json in layered dict with information given
    return 0
