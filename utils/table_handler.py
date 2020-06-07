import logging
from .misc import umlaut

logger = logging.getLogger("app")


def tables_from_soup(soup):
    tables = [
        [
            [td.get_text(strip=True) for td in tr.find_all("td")]
            for tr in table.find_all("tr")
        ]
        for table in soup.find_all("table")
    ]

    return tables


def get_table(name, tables):
    full, form, home, away = tables
    if name == "full":
        return full
    elif name == "form":
        return form
    elif name == "home":
        return home
    elif name == "away":
        return away
    else:
        err_msg = f"Table: {name} is not a valid selection"
        logger.error(err_msg)
        raise Exception(err_msg)


def find_team_in_table(team, table):
    # should find a way to do this in a non n^2 manner
    for row in table:
        for column in row:
            if team.lower() in umlaut(column).lower():
                return row


def extract_table_stats(row):
    _, position, team_name, games_played, wins, ties, losses, goal_diff, points = row
    return position, team_name, games_played, wins, ties, losses, goal_diff, points
