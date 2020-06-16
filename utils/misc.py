from bs4 import BeautifulSoup
from tempfile import TemporaryFile
from the_mines.download.get_html import download_default_html


def umlaut(word_with_umlaut):
    """Insert accented chars where applicable

    Args:
        word_with_umlaut(str): a word containing an umlaut
    Returns:
        word with actual umlaut
    """
    if "\\xc3\\xb6" in word_with_umlaut:
        word_with_umlaut = word_with_umlaut.replace("\\xc3\\xb6", "ö")
    if "\\xc3\\xbc" in word_with_umlaut:
        word_with_umlaut = word_with_umlaut.replace("\\xc3\\xbc", "ü")
    if "\\" in word_with_umlaut:
        word_with_umlaut = word_with_umlaut.replace("\\", "")
    return word_with_umlaut

def open_default_html():
    """Get homepage html containing data for current matchday

    Returns:
        content of title tag as string
    """
    raw_html = download_default_html()
    with TemporaryFile("w+") as tmp:
        tmp.write(raw_html)
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        return = soup.title.text

def get_default_matchday():
    """Returns the current or most recent matchday

    Returns:
        matchday as string (eg. '3')
    """
    title = open_default_html()
    ind = title.index(".")
    matchday = title[ind - 2 : ind]

    return matchday.strip()

def get_default_season():
    """Returns the current or most recent season

    Returns:
        season as string (eg. '2019/2020')
    """
    title = open_default_html()
    ind = title.index("/")
    season = title[ind - 4 : ind + 5]

    return season.strip()
