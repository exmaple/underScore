import requests
import shutil
import os


def get_matchday_html(matchday, season):
    """Download fussballdaten html file

    The URL of this website uses only the latter year in a season (2019/2020).
    `season[5:9]` selects the latter season. I'm using the 2019/2020 convention
    for season input because I believe it is what most users are familiar with
    when asked for a season.

    Args:
        matchday (str): desired matchday
        season (str): desired season

    Returns:
        filename of downloaded html page
    """
    url = "https://www.fussballdaten.de/bundesliga/" + season[5:9] + "/" + matchday

    page_source = requests.get(url)
    season = season.replace("/", "_")
    filename = "fussballdaten_" + season + "_" + matchday + ".html"
    filepath = 'the_mines/data/' + filename

    # Check if file exists
    if not os.path.isfile(filepath):
        with open(filename, "w") as f:
            print("creating file..." + filename)
            f.write(str(page_source.content))
            shutil.move(filename, "the_mines/data/" + filename)
    else:
        print("opening file... " + filename)
        return filename

    return filename
