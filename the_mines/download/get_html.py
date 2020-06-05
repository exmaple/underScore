import requests
import logging


logger = logging.getLogger("app")

def download_default_html():
    url = "https://www.fussballdaten.de/bundesliga/"
    data = str(requests.get(url).content)

    except Exception:
        logger.debug(f"Unable to download file")

    return data

def download_html(matchday, season):
    """Download fussballdaten html file

    The URL of this website uses only the latter year in a season (2019/2020).
    `season[5:9]` selects the latter season. I'm using the 2019/2020 convention
    for season input because I believe it is what most users are familiar with
    when asked for a season.

    Args:
        matchday (str): desired matchday
        season (str): desired season

    Returns:
        data str containing downloaded html page content
    """
    try:
        logger.debug("Downloading data file")
        url = "https://www.fussballdaten.de/bundesliga/" + season[5:9] + "/" + matchday
        data = str(requests.get(url).content)

    except Exception:
        logger.debug(f"Unable to download file using params: {matchday}, {season}")

    return data
