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

def get_default_matchday(matchday_or_season):
    raw_html = download_default_html()
    with TemporaryFile("w+") as tmp:
        tmp.write(raw_html)
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        title = soup.title.text
        if matchday_or_season == 'matchday':
            ind = title.index('.')
            matchday = title[ind-2:ind]
        elif matchday_or_season == 'season':
            ind = title.index('/')
            matchday = title[ind-4:ind+5]

    return matchday.strip()
