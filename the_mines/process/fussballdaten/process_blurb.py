from bs4 import BeautifulSoup
from tempfile import TemporaryFile
import logging
from ...download.get_html import download_raw_html
from utils.misc import umlaut
from utils.table_handler import find_team_in_table, extract_table_stats, tables_from_soup


logger = logging.getLogger("app")


def get_blurb(team, season):
    base = f"https://www.fussballdaten.de/bundesliga/tabelle/{season}"
    logger.debug(f'Hitting {base}')
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(base))
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        # the league table is the first one we get from the html package
        tables = tables_from_soup(soup)
        position, team_name, _, wins, ties, losses, _, points = extract_table_stats(find_team_in_table(team, tables[0]))

    logger.debug(f'Returning blurb stats for {team}')

    return {
        "title": f"{umlaut(team_name)}",
        "fields": {
            "Pos": f"{position}",
            "WTL": f"{wins}-{ties}-{losses}",
            "Pts": f"{points}",
        },
    }
