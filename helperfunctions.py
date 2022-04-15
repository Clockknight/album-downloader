import json
import re
import os

def writable(rewrite):
    """Return given string, after removing all characters that would cause errors."""
    pattern = r'[:<>\*\?\\\/|\"]'
    rewrite = re.sub(pattern, "", rewrite)
    return rewrite


def songlistin(releasesoup):
    """Parse info from release page, return array of songs."""
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


def parsetime(instring):
    """Convert hh:mm:ss strings into int value in seconds."""
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


def checkhistory():
    """Write history.json if it doesn't exist yet. Return the json file opened."""
    historydir = "history.json"

    if not os.path.exists(historydir):
        with open(historydir, 'w') as f:
            json.dump({}, f)

    return open(historydir)


# TODO implement writehistory
def writehistory(giveninfo):
    """Update values in history json with given values."""
    # assume the following:
    # giveninfo is an Information object for one release

    # write the above to the json in layered dict with information given
    # take most recent version of
    newthing = readhistory()

    newthing[giveninfo.artist] =
    newthing["artist"]["album"] = giveninfo.album


# TODO implement readhistory
def readhistory():
    """Return history.json results as a dict."""
    history = {}

    with open('history.json') as f:
        # TODO actually implement JSON read function
        history = json.read(f)

    return history