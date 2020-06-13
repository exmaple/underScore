import logging
from .misc import umlaut

logger = logging.getLogger("app")


def tables_from_soup(soup):
    """Get all tables available from soup parser

    Args:
        soup (BeautifulSoup): HTML parser

    Returns:
        list of tables from html page
    """
    logger.debug("Collecting all tables")
    tables = [
        [
            [td.get_text(strip=True) for td in tr.find_all("td")]
            for tr in table.find_all("tr")
        ]
        for table in soup.find_all("table")
    ]

    return tables


def get_table(tables, full=False, form=False, home=False, away=False):
    """Extract desired table from table set

    By default the "table" page from fussballdaten has 4 tables:
        1. full - the full league table will all teams and stats
        2. form - a table containing teams with the best form (most points) in
                  last 3 matches
        3. home - a table containing teams with best home form (most points) in
                  last 3 home matches
        4. away - a table containing teams with best away form (most points) in
                  last 3 home matches
    The method will only return a single table from these selections.

    Args:
        tables (list): tables from the html parser
        full (bool): option for full table
        form (bool): option for form table
        home (bool): option for home table
        away (bool): option for away table

    Returns:
        selected table
    """
    logger.debug("Collecting target table")
    full_table, form_table, home_table, away_table = tables

    if full:
        return full_table
    elif form:
        return form_table
    elif home:
        return home_table
    elif away:
        return away_table
    else:
        err_msg = f"Table: {name} is not a valid selection"
        logger.error(err_msg)
        raise Exception(err_msg)


def find_team_in_table(team, table):
    """Given a table get a team's stats row

    Args:
        team (str): target team
        table (list): rows of table

    Returns:
        target team's statistical row
    """
    logger.debug("Searching for team in table")
    # should find a way to do this in a non n^2 manner
    for row in table:
        for column in row:
            if team.lower() in umlaut(column).lower():
                return row

    logger.debug(f"Target team: {team}, not found")
    return None


def extract_full_table_stats(row):
    """Collects all statics avaiable to full table

    Args:
        row (list): statistical row from full table

    Return:
        all known stats in row
    """
    logger.debug("Extracting full table stats")
    _, position, team_name, games_played, wins, ties, losses, goals_for_against, goal_diff, points = row
    return position, team_name, games_played, wins, ties, losses, goals_for_against, goal_diff, points
