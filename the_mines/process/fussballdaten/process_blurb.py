from bs4 import BeautifulSoup
from tempfile import TemporaryFile
import logging
from ...download.get_html import download_raw_html
from utils.misc import umlaut
from utils.table_handler import (
    find_team_in_table,
    extract_full_table_stats,
    tables_from_soup,
    get_table
)


logger = logging.getLogger("app")


def get_blurb(team, season='2020'):
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
        position, team_name, _, wins, ties, losses, _, points = extract_full_table_stats(
            find_team_in_table(team, table)
        )

    logger.debug(f"Blurb stats colected for {team}")

    return {
        "title": f"{umlaut(team_name)}",
        "fields": {
            "Pos": f"{position}",
            "WTL": f"{wins}-{ties}-{losses}",
            "Pts": f"{points}",
        },
    }
