from bs4 import BeautifulSoup
from tempfile import TemporaryFile
import logging
from ...download.get_html import download_raw_html
from utils.misc import umlaut, format_date
from utils.table_handler import (
    find_team_in_table,
    extract_full_table_stats,
    tables_from_soup,
    get_table,
)
import re


logger = logging.getLogger("app")


def build_score(title, score):
    _, team1, _, team2, date, comp = title.split(" ")
    team1 = umlaut(team1)
    team2 = umlaut(team2)
    # remove trailing bracket
    comp = comp[:-1]
    date = format_date(date[1:-1])
    return f"{team1} {score} {team2}", date, comp


def build_matchup(title):
    # Vorschau & Statistiken: Bremen gegen Bayern (16.06.2020, Bundesliga)
    _, _, _, team1, _, team2, date, comp = title.split(" ")
    team1 = umlaut(team1)
    team2 = umlaut(team2)
    # remove trailing bracket
    comp = comp[:-1]
    date = format_date(date[1:-1])
    return f"{team1} vs. {team2}", date, comp


def get_team_str(target):
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


def get_glance_schedule(team, season="2020"):
    team = get_team_str(team)
    url = f"https://www.fussballdaten.de/vereine/{team}/{season}/spielplan/"
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(url))
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        matches = soup.find_all('a', attrs={'class': re.compile('ergebnis')})
        prev, curr = matches[-2:]
        final_p, half_time_p = prev.find_all('span')
        final_c, half_time_c = curr.find_all('span')

        prev_result, date_p, comp_p = build_score(prev.attrs['title'], final_p.get_text())
        curr_result, date_c, comp_c = build_score(curr.attrs['title'], final_c.get_text())

    # get next section
    url = f"https://www.fussballdaten.de/vereine/{team}/{season}/"
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(url))
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        upcoming, = soup.find_all('div', attrs={'class': 'naechste-spiele'})
        next, _, _ = upcoming.find_all('a')
        matchup, date_n, comp_n = build_matchup(next.attrs['title'])

    results = {
        f"{date_p} ({comp_p})": f"{prev_result}",
        f"{date_c} ({comp_c})": f"{curr_result}",
        f"{date_n} ({comp_n})": f"{matchup}",
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
            "W-T-L": f"{wins}-{ties}-{losses}",
            "Pts": f"{points}",
        },
    }

    results['fields'].update(schedule)
    return results
