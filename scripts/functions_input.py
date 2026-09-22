import scripts.interface as interface
# TODO
# this should be some of the more manual functions from functions_parsing
# with an additional variable to track tkinter labels
# and should update that label instead of printing
# these should also run without arguments, probably
# if they do, then it'll have to ping back to the interface functions to get a textbox and entry



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
        filedir = interface.await_response('Please enter the directory of the text file that has the links to appropriate files separated by '
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

def album_search():
    pass


def artist_search():
    search_process(artist_search=False)



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


def scouting_toggle():
    global scouting
    scouting = not scouting



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
