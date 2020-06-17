from bs4 import BeautifulSoup
from tempfile import TemporaryFile
import logging
from ...download.get_html import download_raw_html
from utils.misc import umlaut, format_date, get_default_season
from utils.table_handler import (
    find_team_in_table,
    extract_full_table_stats,
    tables_from_soup,
    get_table,
)
import re


logger = logging.getLogger("app")


def build_matchup(title, score=None):
    """Build display string given a title

    Args:
        title (str): title information from html page
        score (str): match result

    Returns:
        dict containing formatted field title and score string
    """
    # Pull in items we are interested in from title str
    match = re.search(".*: (.*) gegen (.*) \((.*), (.*)\)", title, re.IGNORECASE)

    team1 = umlaut(match.group(1))
    team2 = umlaut(match.group(2))
    date = format_date(match.group(3))
    comp = match.group(4)

    if not score:
        score = "vs"

    return {f"{date} ({comp})": f"{team1} {score} {team2}"}


def get_team_str(target):
    """Given a team get the string needed to use url

    This is NOT the way we would like to be doing this.  That being said it
    seems like for now it is the only way to collect these particular strings.

    Args:
        target (str): desired team

    Returns:
        string used by url for specific team
    """
    target = target.lower()
    return {
        "bayern": "fc-bayern-muenchen",
        "dortmund": "borussia-dortmund",
        "leipzig": "rb-leipzig",
        "leverkusen": "bayer-leverkusen",
        "m'gladbach": "borussia-moenchengladbach",
        "wolfsburg": "vfl-wolfsburg",
        "hoffenheim": "1899-hoffenheim",
        "freiburg": "sc-freiburg",
        "schalke": "fc-schalke-04",
        "frankfurt": "eintracht-frankfurt",
        "hertha": "hertha-bsc",
        "koln": "1-fc-koeln",
        "augsburg": "fc-augsburg",
        "berlin": "1-fc-union-berlin",
        "mainz": "1-fsv-mainz-05",
        "dusseldorf": "fortuna-duesseldorf",
        "bremen": "sv-werder-bremen",
        "paderborn": "sc-paderborn-07",
    }[target]


def get_glance_schedule(team, season=get_default_season()):
    team = get_team_str(team)

    # Get previous and current match
    url = f"https://www.fussballdaten.de/vereine/{team}/{season}/spielplan/"
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(url))
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        # List of matches
        matches = soup.find_all("a", attrs={"class": re.compile("ergebnis")})

        # We are interested in the 2 most recent results
        prev, curr = matches[-2:]

        # Get scores
        prev_score, _ = prev.find_all("span")
        curr_score, _ = curr.find_all("span")

    # Get next match
    url = f"https://www.fussballdaten.de/vereine/{team}/{season}/"
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(url))
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        (upcoming,) = soup.find_all("div", attrs={"class": "naechste-spiele"})

        # The list of upcoming matches depends on how many matches are left
        # in the season.  We can't reliably list decompose so we'll have to pop
        next = upcoming.find_all("a").pop(0)

    results = {}
    results.update(build_matchup(prev.attrs["title"], prev_score.get_text()))
    results.update(build_matchup(curr.attrs["title"], curr_score.get_text()))
    results.update(build_matchup(next.attrs["title"]))

    return results


def get_glance_table_stats(team, season=get_default_season()):
    """Get table statistics for blurb

    Args:
        team (str): target team
        season (str): target season

    Results:
        dict containing table stats
    """
    url = f"https://www.fussballdaten.de/bundesliga/tabelle/{season}"
    logger.debug(f"Hitting {url}")
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(url))
        tmp.seek(0)

        # parse html output for tables
        soup = BeautifulSoup(tmp, "html.parser")
        table = get_table(tables_from_soup(soup), full=True)

        # collect target statistics from target team
        (
            position,
            team_name,
            _,
            wins,
            ties,
            losses,
            _,
            _,
            points,
        ) = extract_full_table_stats(find_team_in_table(team, table))

        return {
            "title": f"{umlaut(team_name)}",
            "fields": {
                "Pos": f"{position}",
                "W-T-L": f"{wins}-{ties}-{losses}",
                "Pts": f"{points}",
            },
        }


def get_blurb(team):
    """Gets a selection of stats for a team

    Args:
        team (str): name of team
        season (str): target season

    Returns:
        dictionary containing team as title and selection of statistical fields
    """
    results = {}
    results.update(get_glance_table_stats(team))
    results["fields"].update(get_glance_schedule(team))

    logger.debug(f"Blurb stats colected for {team}")
    return results
