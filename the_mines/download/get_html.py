import requests


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
        url = "https://www.fussballdaten.de/bundesliga/" + season[5:9] + "/" + matchday
        data = str(requests.get(url).content)

    except Exception:
        print(f"Unable to download file using params: {matchday}, {season}")

    return data
