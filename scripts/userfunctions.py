from json import JSONDecodeError
import eyed3
import urllib
import requests
import shutil
import pytube
from pytube import YouTube, Search
from bs4 import BeautifulSoup
from moviepy.editor import *
from scripts.classes import *
import json
import re
import os

# TODO Fix the console only printing out part of the artist's name when downloading GG OST
# TODO replace more text in console when going through release
# TODO Include album #/# when printing "downloading album" message
# TODO include "artist (###)" in perfect match results in search_process()
"""
First pass, look for each word in the release name, song name in the title, artist name in title and channel name
Second pass, also look through the videos' descriptions when looking for words in title, release name, artist name
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def option_select():
    """Text menu for user to choose option"""
    option = input('''
Welcome to Clockknight's Album Downloader. Please choose from an option below by entering the option number:

1) Cache Mode
Provide a .txt file with names of artists or releases, seperated by lines.

2) Search Mode (Artist)
Search for an artist's discography. The artist's discography will be stored in history.json

3) Search Mode (Album)
Search for an album. Recommended for albums with generic artist like "Various".

4) Update
Will check for new releases from artists that you have used this script to look at before. 

5) Ignorant Download
Will download each song in every release, even if it has been previously downloaded. 

8) URL Mode
Paste in a YouTube URL, and the program will download it.

9) Settings
Change the settings of the script.

0) Exit

    ''')

    match option:
        case '1':
            cache_input()
        case '2':
            search_process()
        case '3':
            search_process(artist_search=False)
        case '4':
            update()
        case '5':
            ignorant_download()
        case '8':
            url_input()
        case '9':
            update()
        case '0':
            sys.exit()
        case _:
            print('Invalid option selected. Please try again.\n\n')

    return True


# Functions that take input from user, or determine logic of usage of below functions
def cache_input(filedir=None):
    # TODO enable test inputs on this function
    """
    Keyword Arguments:

    filedir -- directory of cache text file (default None)

    Take multiple inputs from text file, ask user if given input is artist or release.
    """
    cache_dict = {}

    if filedir is None:
        filedir = input(
            'Please enter the directory of the text file that has the links to appropriate files separated by '
            'newlines.\n')

    # parses each line as new input, prompts user to clarify if each line is an artist or a user
    # Use read_lines to separate out the links of albums
    items = open(filedir, 'r').read().splitlines()
    for item in items:
        artist_search = 3
        while artist_search not in range(-1, 2):
            artist_search = int(input(
                """Item: 
    {} 

Input -1 to skip.
Input 0 if this is an artist.
Input 1 if it is a release.""".format(item)))

        if artist_search == -1:
            continue
        else:
            artist_search = artist_search == 0

        returned_url = get_user_option(artist_search, item)
        if returned_url is None:
            continue
        cache_dict[returned_url] = artist_search

        print(cache_dict)

    # below is current implementation:
    # search process -> download list of songs
    for query_key in cache_dict:
        new_information = search_process(query=query_key, artist_search=cache_dict[query_key])
        append_history(new_information)


def url_input(url=None):
    """Download given YouTube URL as MP3."""
    info_object = Information()
    info_object.setup_url()
    os.makedirs(info_object.target_storage, exist_ok=True)  # Make the folder
    if url is None:
        url = input('\nPlease input the url of the video you want to download.\n\t')

    try:
        # Declare yt_obj now to declare info_object.art as the YouTube thumbnail
        yt_obj = YouTube(url)
        info_object.art = yt_obj.thumbnail_url
        return download_song(yt_obj, info_object)
    except pytube.exceptions.VideoUnavailable or pytube.exceptions.RegexMatchError:
        input("Invalid URL. Press Enter to return to the main menu.")


def update():
    """Check releases and artists for yet to be downloaded songs. Call append_history."""
    info_object = Information()
    history = read_history(info_object)
    for artist in history:
        search_process("artist", artist)


def ignorant_download():
    # check historyjson
    history = read_history(Information())

    # write each artist's history as {}
    for artist in history:
        history[artist] = {}
    append_history(Information(), history)
    # then update
    update()


# Functions to parse information


def search_process(query=None, artist_search=True, info_object=None):
    """
    Keyword Arguments:

    query -- artist/release to be searched

    artist_search -- boolean describing if this is an artist search (default to True)

    info_object -- Information object with any previous history (default to None)

    Assume url to be scraped has already been selected, and pass on information to the correct function.

    Return: Information object, storing a record of the songs downloaded.
    """


    # Get input for artist/album name when no term is passed
    if info_object is None:
        info_object = Information()

    if query is None:
        query = input("Please input the name of the {} you're searching for:\n".format("artist" if artist_search else "release"))

    if artist_search:
        # Only artist mode has multipage support (Not an issue yet?)
        info = parse_artist("https://discogs.com/search/?q=" + query + "&type=artist&page=", info_object)
    else:
        info = process_release("https://discogs.com" + query)

    # TODO make search_process return an info object
    # In order to do this, make downloadlistofsongs return an info object
    return download_list_of_songs(info)


def parse_artist(query, info_object):
    """
    Keyword Arguments:

    query -- url to be searched

    info_object -- Information object with any previous history (default to None)

    Parse artist, calling parse_artist_page() for each page.

    Return: formatted list of songs downloaded.
    """
    # TODO include method to get releases the artist is only credited in
    index = 1
    releases = []
    while True:
        # store array of releases to download
        try:
            result = parse_artist_page(query + str(index))
            if result is None:
                break
            releases += result
        except AttributeError as e:
            print(e)
            print("Please copy console output and send to the issues page.")
            break
        index += 1
        # if nothing is returned from above, break out (query for parse_artist_page was an empty page)
        if not releases:
            break

    read_history(info_object)
    for release in releases:
        processed_info = process_release(release, info_object)
        info_object.update(processed_info)

    return info_object


def parse_artist_page(query):
    """Parse a single page of releases on an artist's page. Return array of release URLs."""
    results = []
    soup = requests.get(query, headers=headers)
    soup = BeautifulSoup(soup.text, "html.parser")

    # < table class ="cards table_responsive layout_normal" id="artist" >
    table = soup.find("table", id="artist")
    if table is None:
        return None
    trs = table.find_all("tr")
    for tr in trs:
        # Every tr with an album has this attribute
        if tr.has_attr("data-object-type"):
            tr = tr.find("a")
            results.append("https://discogs.com" + tr["href"])
    return results


def process_release(query: str, current_information=Information()):
    """
    Keyword Arguments:

    query -- url of a discogs release

    current_information -- information about the release (default new Information)

    Parse information for release. Adjust incoming Information properties to match query

    Return: Most current data of release.
    """
    # TODO Check if multiple versions from different artists exist, get one with most songs

    #  tryexcept for passed query
    try:
        page = requests.get(query, headers=headers)  # Use requests on the new URL
        if page.status_code != 200:
            raise ConnectionError(page.status_code)
        soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
    except ConnectionError as e:
        print(e)
        print('Error: failure processing album. Link provided - ' + query)
        print("Connection Error. Copy Console Output and talk about it in the issues page.")
        return current_information

    name = soup.find('h1', {"class", "title_1q3xW"})  # grabs artist and album
    artist_name = name.find('a').text
    artist_search= True
    # ToDO Fix other people being included into history when some releases have the current artist as a side artist
    # going to need to move this outside of the scope of this function so it doesnt guess
    if current_information.artist is None:
        artist_search = False
    current_information.set_artist(artist_name)  # separate artist
    current_information.album = name.text[
                                len(artist_name) + 3:]  # grab album by removing enough characters from above var

    print('\n\tDownloading Album - ' + current_information.album)
    coverart = soup.find('div', {"class": "more_8jbxp"})  # finds url in the <a> tag of the cover preview
    try:
        art_url = "https://discogs.com" + coverart.find('a')['href']
        current_information.art = requests.get(art_url)
        if current_information.art.status_code != 200:
            raise ConnectionError(current_information.art.status_code)
    except ConnectionError as e:
        # Let the user know the album art isn't available
        # TODO this pings every release - figure out why
        print('\t\tMissed Tag: Problem getting album art - {} - {}'.format(e.args[0], current_information.album))
        current_information.art = 'fail'  # set it to fail for mp3 tag check

    # Preparing directory to download song
    # create folder for artist, and subdirectory for release
    current_information.set_storage()
    os.makedirs(current_information.target_storage, exist_ok=True)  # Make the folder
    current_information.songs = song_list_in(soup)
    # TODO calling read history every time i process a release is probably killing run time, fix it. Make a single call somewhere.
    # in the single call make a big dict that stores Informations as they get returned and then store them bsaed on artist name

    if artist_search:
        old_information = Information()
        old_information.success = read_history(current_information)
        return old_information

    # TODO changed this to return current information - might be causing ALL downloads to fail
    return current_information
    # download_list_of_songs()

    # Call to write history to UPDATE with the songs that have been downloaded.


# Functions that download albums or songs, after parsing info

def download_list_of_songs(info_object):
    """
    Keyword Arguments:

    info_object -- Information object with prior history of release (default to None)

    Send pytube YouTube objects to download song.

    Return: Return Information with success and failed songs
    """

    info_object.song_count = 0
    info_object.total_count = len(info_object.songs)
    # mega Codeblock to download array's songs
    # Use album name + song name + "song" in YouTube search

    for song_name in info_object.songs:
        info_object.current_song = song_name
        print('\t\tDownloading - ' + song_name)

        res = Search(writable(info_object.album + ' ' + info_object.artist + ' song ' + song_name))
        res.results
        loop = len(res.results)
        # loop to check at least 100 videos, get_next_results does not pull consistent amount of videos
        while loop < 100:
            res.get_next_results()
            loop = len(res.results)
        res = res.results

        song_length = info_object.songs[song_name]
        if song_length == 0:
            print('\r\t\tNo song length found. Result may be inaccurate.')

        # Nested if checks to see if artist, album, and song are all used
        if info_object.artist in info_object.history:
            temp = info_object.history[info_object.artist]
            if info_object.album in temp:
                temp = temp[info_object.album]
                if song_name in temp:
                    print('\r\t\tSong Previously Downloaded, Skipping...', flush=True)
                    continue

        videos = loop

        for video in res:  # Go through videos pulled
            mismatched = False
            print('\r\t\tAttempting video ' + str(videos - loop + 1) + '/' + str(videos), end='\r', flush=True)
            loop -= 1
            # Range is 85% to 110% of the song length
            try:
                vid_length = video.length
                # Filter for video codeblock
                if vid_length not in range(int(song_length * .85), int(song_length * 1.25)) and song_length != 0:
                    continue  # Try again with next video if it's out of range
            except TypeError:
                print("Video length error. Usually caused when looking at an archived stream.")

            if search_result_filter(info_object, video):
                break

        # check, catches if no videos in first results are
        if loop == 0:
            print('\t\tFailed Download: No result found within parameters - ' + song_name)  # let user know about this
            continue  # move onto next song_name in this case

        print('\r\t\tDownloading...', end="\r", flush=True)

        # clean_name is directory of mp4
        info_object.song_count += 1  # increment song_count once song is found, before downloading it

        # Add song to successful songs if download_song returns true
        try:
            if os.path.exists(download_song(video, info_object)):
                info_object.update_success({song_name: song_length})

        # Skip to next song if above block raises an error
        except pytube.exceptions.VideoUnavailable:
            print("blahblah")
            print('\t\tFailed Download: issue downloading from YouTube - ' + song_name)
            continue

    append_history(info_object)

    return info_object


def download_song(yt_obj, info_object):
    """Download MP3 from YouTube object. Return Bool based on if download was successful.
    Download as MP4 for now. Downloading the MP3 stream given causes issues when trying to edit MP3 tags."""
    # TODO  Find way to cut off dead air before and after song plays
    try:
        video = yt_obj.streams.filter(type="video")
    except KeyError:
        return False
    video = video.order_by("abr").desc().first()

    videopath = os.path.abspath(os.path.join(info_object.target_storage, writable(video.title))) + '.mp4'
    video.download(filename=videopath)

    clip = AudioFileClip(videopath)  # make var to point to mp4's audio
    clip.fx(afx.audio_normalize)
    audio_file_path = videopath[:-1] + '3'  # audio_file_path points to where the mp3 file will be
    clip.write_audiofile(audio_file_path, logger=None)  # write audio to audio path

    os.remove(videopath)  # delete old mp4

    if info_object.is_album:
        tag_song(audio_file_path, info_object)

    print('\r', end='')

    return audio_file_path


def tag_song(target, info_object):
    """Tag MP3 with given information. Also normalizes the audio of the file."""
    tag_target = eyed3.load(target)  # creates mp3audiofile at downloaded mp3
    tag_target = tag_target.tag
    tag_target.title = info_object.current_song
    tag_target.artist = info_object.artist
    tag_target.album = info_object.album
    tag_target.album_artist = info_object.artist
    tag_target.track_num = (info_object.song_count, info_object.total_count)
    if info_object.art != 'fail':  # Check if coverart is actually valid
        coverart = info_object.art.url

        filename = os.path.join(info_object.target_storage, writable(info_object.album) + ".jpg")
        r = requests.get(coverart, stream=True)
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        with open(filename, "rb") as f:
            tag_target.images.set(3, f.read(), "image/jpg")
        info_object.art = "fail"

        os.remove(filename)

    tag_target.save(target)


# Helper functions

def writable(rewrite):
    """Return given string, after removing all characters that would cause errors."""
    pattern = r'[:<>\*\?\\\/|\/"]'
    rewrite = re.sub(pattern, "", rewrite)
    return rewrite.strip()


def song_list_in(release_soup):
    """Parse info from release page, return dict of songs and song lengths."""
    result = {}
    # find table with class, tbody inside

    # regex for tracklist_[5 alphanumeric chars]
    regex_pattern = r"tracklist_\w{5}"
    table = release_soup.find("table", {"class": re.compile(regex_pattern)})
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


def check_history(info_object=Information()):
    """Assume:
        User wants history file at location. Location informed by Information object.
    Write history.json if it doesn't exist yet. Return the directory to the file opened."""
    history_directory = info_object.history_storage
    if history_directory is None:
        info_object.history_storage, history_directory = ".\\assets\\history.json"  # default history location

    if not os.path.exists(history_directory):
        with open(history_directory, 'w') as f:
            json.dump({}, f)

    return info_object


def append_history(info_object, overwrite_hist=None):
    """Assume:
        info_object is an Information object with information on new songs that have been downloaded.
        History.json file exists
    Update values in history.json with given values.
    If overwriteHist is specified, overwrite history.json with it"""

    # Case where no overwrite history is provided
    history_directory, new_history = info_object.history_variables()
    total_hist = read_history(info_object)
    current_artist = info_object.artist
    # Check if the artist dict in history needs to be overwritten
    # TODO fix program crashing here since it's comparing none to string
    if overwrite_hist is None:
        if current_artist in total_hist:
            if len(total_hist[current_artist]) == 1:
                if info_object.album in total_hist[current_artist]:
                    # if the last two tests passed that means this is the first release to be processed, and this is the second append_history call on that release
                    total_hist[current_artist][info_object.album] = {}
            total_hist[current_artist].update(new_history[current_artist])
        else:
            total_hist.update(new_history)
    else:
        total_hist = overwrite_hist

    result = json.dumps(total_hist, sort_keys=True, indent=4)

    # write result to the file
    f = open(history_directory, 'w')
    f.write(result)
    f.close()


def read_history(info_object=Information()):
    """Return artist's results from history.json as a dict.
    If no artist is specified, return all results."""
    hist_dir = info_object.history_storage
    if not os.path.exists(hist_dir):
        open(hist_dir, 'w+')
    f = open(hist_dir, 'r')

    try:
        result = json.load(f)
    # except for general json issue
    except JSONDecodeError:
        return {}
    return result


def parsetime(in_string):
    """Convert hh:mm:ss strings into int value in seconds."""
    if re.fullmatch("\d[\d:]*\d", in_string) is None:
        raise Exception
    numbers = in_string.split(":")
    iteration = len(numbers) - 1
    result = 0

    for value in numbers:
        value = int(value)
        match iteration:
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
        iteration -= 1

    return result


def get_user_option(artist_search, search_term):
    """
    Keyword Arguments:

    artist_search -- boolean to clarify if search is for artist or release

    search_term -- the name of the artist or release being checked

    Print out all of an array's items, then ask user for an option. Seperate large lists of options into pages.

    Return: url of user-selected page. If user exits, returns None.
    """

    # todo get_user_option returns none when using albums
    # imported block
    titles = []
    matches = []
    search_term = search_term.lower()
    info_object = Information()
    if artist_search:
        info_object.set_artist(search_term)
    # Makes artist string OK for URLs
    url_term = urllib.parse.quote_plus(search_term)
    query = 'https://www.discogs.com/search/?q=' + url_term + '&type=' + ('artist' if artist_search else 'release')
    page = requests.get(query, headers=headers)

    # Codeblock for scraping discogs
    soup = BeautifulSoup(page.text, "html.parser")  # Take requests and decode it
    # Creates a list from all the divs that make up the cards
    elems = soup.find_all('li', {"role": "listitem"})
    # Go through each div, each one has a release/artist with a link out
    for e in elems:
        result = e.find('div', {"class": "card-release-title"}).find('a')
        title = result['title'].lower()
        # If looking for artist, it takes first perfect match and escapes
        if title == search_term:  # compare input to card's title
            if not artist_search:
                artist = e.find('div', {"class": "card-artist-name"}).find('a')['title'].lower()
                title += " - {}".format(artist)
            titles.append(title)
            matches.append(result)

    length = len(matches)
    displayed_per_page = 20
    page_count = -1
    display = ""
    # Return 0 or 1 if the array is empty or has 1 object respectively
    if not length:
        return None
    elif length == 1:
        return matches[0]["href"]

    while True:

        if page_count >= int(length / displayed_per_page):
            page_count = -1

        page_count += 1

        current_page = range(displayed_per_page * page_count ,
                             min(length, displayed_per_page * (page_count + 1) + 1))

        for i in current_page:
            display += str(i+1) + ": " + titles[i - 1] + "\n"

        if length > displayed_per_page:
            display += "Input a number outside of the current displayed to show the next {} results.".format(
                displayed_per_page)

        option = int(input(display))
        if option in current_page:
            return matches[option - 1]["href"]
        # else:
        # todo implement logic to make this loop

        '''# goes here if user_option returns 0
        if isinstance(result, list):
            i = get_user_option(result)
            if i:
                result = result[i - 1]'''


def search_result_filter(info_object, video):
    """Given information from the info_object, check if the video is within expectations of the song.
    """
    # TODO make multiple passes through each video when looking through a song to increase filter accuracy
    '''
    Stages of filtering
    
    '''

    # retrieve
    artist_filter, album_song_filter = info_object.filter_words()
    fail_words = []

    try:
        video_name = video.title.split()
    except Exception as e:
        print(e)
        return False
    for i in range(len(video_name)):
        video_name[i] = video_name[i].lower()

    for word in info_object.current_song.split():
        temp = False
        for vid_word in video_name:
            if not temp and word.lower() in vid_word:
                temp = True
                break
        # immediately return false if it can't be found in any of video_name's words
        if not temp:
            return False

    # Try to find word in title
    # if it's not in title, track it, then check description
    for word in artist_filter:
        for vid_word in video_name:
            if not temp and word.lower() in vid_word:
                fail_words.append(word)
                break

    # Only enter this loop if filter_words isn't empty
    if fail_words:
        desc_words = video.description.split()
        for word in fail_words:
            temp = False
            for dword in desc_words:
                if word in dword:
                    temp = True
                    break
            if not temp:
                return False

    # return true if code reaches here
    return True


# Used for testing
def clear_history():
    f = open("assets/history.json", 'w')
    f.write("")
