from bs4 import BeautifulSoup
from tempfile import TemporaryFile
import logging
from ...download.get_html import download_raw_html
from utils.misc import umlaut


logger = logging.getLogger("app")


def find_team_in_table(team, table):
    # should find a way to do this in a non n^2 manner
    for row in table:
        for column in row:
            if team.lower() in umlaut(column).lower():
                return row


def get_blurb(team, season):
    base = f"https://www.fussballdaten.de/bundesliga/tabelle/{season}"
    logger.debug(f'Hitting {base}')
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(base))
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        # get all tables
        tables = [
            [
                [td.get_text(strip=True) for td in tr.find_all('td')]
                for tr in table.find_all('tr')
            ]
            for table in soup.find_all('table')
        ]

        # the league table is the first one we get from the html package
        table_stats = find_team_in_table(team, tables[0])

    logger.debug(f'Returning blurb stats for {team}')

    return umlaut(table_stats[2]), {
        "Position": f"{table_stats[1]}",
        "W-T-L": f"{table_stats[4]}-{table_stats[5]}-{table_stats[6]}",
        "Points": f"{table_stats[8]}",
    }
