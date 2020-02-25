import requests
import shutil
import os


def get_html(matchday, season):

    # - The URL of this website uses only the latter year in a season (2019/2020).
    # - season[5:9] selects the latter season.
    # - I'm using the 2019/2020 convention for season input because I believe it
    #   is what most users are familiar with when asked for a season
    url = "https://www.fussballdaten.de/bundesliga/" + season[5:9] + "/" + matchday

    page_source = requests.get(url)
    season = season.replace("/", "_")
    filename = "fussballdaten_" + season + "_" + matchday + ".html"
    filepath = 'data/' + filename

    # Check if file exists
    if not os.path.isfile(filepath):
        with open(filename, 'w') as f:
            print("creating file..." + filename)
            f.write(str(page_source.content))
            shutil.move(filename, "data/" + filename)
    else:
        print("opening file... " + filename)
        return filename

    return filename # should this be in the if statement or out here?


if __name__ == "__main__":

    get_html(matchday, season)
