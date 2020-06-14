from bs4 import BeautifulSoup
from tempfile import TemporaryFile
import logging
from ...download.get_html import download_raw_html
from utils.misc import umlaut
from utils.table_handler import (
    find_team_in_table,
    extract_full_table_stats,
    tables_from_soup,
    get_table,
)
import re


logger = logging.getLogger("app")


def build_score(title, score):
    _, team1, _, team2, _, comp = title.split(" ")
    # remove trailing bracket
    comp = comp[:-1]
    return f"{team1} {score} {team2}", comp



def get_glance_schedule(team, season="2020"):
    # url = f"https://www.fussballdaten.de/vereine/fc-bayern-muenchen/{season}/"
    url = f"https://www.fussballdaten.de/vereine/fc-bayern-muenchen/{season}/spielplan/"
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(url))
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        # get curr as well
        matches = soup.find_all('a', attrs={'class': re.compile('ergebnis')})
        prev, curr = matches[-2:]
        final_p, half_time_p = prev.find_all('span')
        final_c, half_time_c = curr.find_all('span')

        prev_result, comp_p = build_score(prev.attrs['title'], final_p.get_text())
        curr_result, comp_c = build_score(curr.attrs['title'], final_c.get_text())

        results = {
            f"Previous Match ({comp_p})": f"{prev_result}",
            f"Current Match ({comp_c})": f"{curr_result}",
        }

        return results


def get_blurb(team, season="2020"):
    """Gets a selection of stats for a team

    Args:
        team (str): name of team
        season (str): target season

    Returns:
        dictionary containing team as title and selection of statistical fields
    """
    base = f"https://www.fussballdaten.de/bundesliga/tabelle/{season}"
    logger.debug(f"Hitting {base}")
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(base))
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

        schedule = get_glance_schedule(team)

    logger.debug(f"Blurb stats colected for {team}")

    results = {
        "title": f"{umlaut(team_name)}",
        "fields": {
            "Pos": f"{position}",
            "WTL": f"{wins}-{ties}-{losses}",
            "Pts": f"{points}",
        },
    }

    results['fields'].update(schedule)
    return results
