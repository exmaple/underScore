import datetime
from the_mines.download.get_html import download_raw_html
from tempfile import TemporaryFile
from bs4 import BeautifulSoup
from unidecode import unidecode


def umlaut(word):
    """Insert accented chars where applicable

    Args:
        word (str): a word containing an umlaut
    Returns:
        word with actual umlaut or just word
    """
    if "\\xc3\\xb6" in word:
        return word.replace("\\xc3\\xb6", "ö")
    elif "\\xc3\\xbc" in word:
        return word.replace("\\xc3\\xbc", "ü")
    else:
        return word


def unumlaut(word):
    """Insert letter where accented chars are meant to be

    This is the opposite of the `umlaut` function.  Rather than adding the
    accent, we are placing the non-accented letter.

    Args:
        word (str): a word containing an umlaut
    Returns:
        word with regular letter
    """
    if "\\xc3\\xb6" in word:
        return word.replace("\\xc3\\xb6", "o")
    elif "\\xc3\\xbc" in word:
        return word.replace("\\xc3\\xbc", "u")
    else:
        # This tool will replace any accented chars with non-accented chars
        return unidecode(word)


def get_author_info(ctx):
    """Collect command caller info

    Args:
        ctx (Context): calling context

    Returns:
        dict with name and avatar
    """
    return {
        "name": ctx.author.display_name,
        "icon_url": ctx.author.avatar_url,
    }


def format_date(date):
    """Given a date string from fussballdaten format nicely

    Args:
        date (str): date string

    Returns:
        formatted date string
    """
    day, month, year = date.split(".")
    game_date = datetime.date(int(year), int(month), int(day))
    month_name = game_date.strftime("%B")
    return f"{month_name} {day}, {year}"


def get_default_season():
    """Returns the current or most recent season

    Returns:
        season as string (eg. '2019/2020')
    """
    raw_html = download_raw_html("https://www.fussballdaten.de/bundesliga/")
    with TemporaryFile("w+") as tmp:
        tmp.write(raw_html)
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        title = soup.title.text
        ind = title.index("/")
        opening, closing = title[ind - 4 : ind + 5].strip().split('/')

    return closing
