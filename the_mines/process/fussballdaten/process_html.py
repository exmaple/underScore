from bs4 import BeautifulSoup
from argparse import ArgumentParser
from tempfile import TemporaryFile
import logging
from ...download.get_html import download_raw_html


logger = logging.getLogger("app")


def get_matchday_results(matchday, season):
    raw_html = download_raw_html(matchday, season)
    return process_results(raw_html)


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


def process_results(raw_html):
    """Scrape html for matchday results using BeautifulSoup

    Args:
        site_html(str): raw html of the website containing the matchday data

    Returns:
        dictionary containing team matchups and the corresponding score
        e.g. {0: [('Team Name', 'Score'),('Team Name', 'Score')], ... }
    """
    with TemporaryFile("w+") as tmp:
        tmp.write(raw_html)
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        # game_count: used as a key in the dictionary of matches
        game_count = 0
        game_dict = {}

        # Returns all 'a' tags within the html in a list. Equivalent to .find_all()
        a_tag = soup("a")

        # Loop through every tag returned and determine whether it contains the
        # data we require.
        for game_details in a_tag:
            if "id" in game_details.attrs and "class" in game_details.attrs:
                teams_list = []
                teams_string = game_details.get("title")
                teams_string_list = teams_string.split()
                counter = 0
                score1 = -1
                score2 = -1
                for scores in game_details:
                    if counter == 1:
                        break
                    scores = str(scores.text)
                    score1 = scores[0]
                    score2 = scores[2]
                    counter += 1

                # When the data is found we need to do some extra string
                # manipulating to ensure the correct team name is returned.
                if teams_string_list[2] == "gegen" and len(teams_string_list) == 6:
                    # 1/1
                    team1 = umlaut(teams_string_list[1])
                    team2 = umlaut(teams_string_list[3])
                    teams_list.append((team1, score1))
                    teams_list.append((team2, score2))
                elif teams_string_list[3] == "gegen" and len(teams_string_list) == 7:
                    # 2/1
                    team1 = teams_string_list[1] + " " + teams_string_list[2]
                    team2 = teams_string_list[4]
                    team1 = umlaut(team1)
                    team2 = umlaut(team2)
                    teams_list.append((team1, score1))
                    teams_list.append((team2, score2))
                elif teams_string_list[2] == "gegen" and len(teams_string_list) == 7:
                    # 1/2
                    team1 = teams_string_list[1]
                    team2 = teams_string_list[3] + " " + teams_string_list[4]
                    team1 = umlaut(team1)
                    team2 = umlaut(team2)
                    teams_list.append((team1, score1))
                    teams_list.append((team2, score2))
                elif teams_string_list[3] == "gegen" and len(teams_string_list) == 8:
                    # 2/2
                    team1 = teams_string_list[1] + " " + teams_string_list[2]
                    team2 = teams_string_list[4] + " " + teams_string_list[5]
                    team1 = umlaut(team1)
                    team2 = umlaut(team2)
                    teams_list.append((team1, score1))
                    teams_list.append((team2, score2))

                game_dict[game_count] = teams_list
                game_count += 1

    return game_dict


def umlaut(word):
    """Insert accented chars where applicable

    Args:
        word (str): a word containing an umlaut
    Returns:
        word with actual umlaut or just word
    """
    if "\\xc3\\xb6" in word:
        return word.replace("\\xc3\\xb6", "ö")
    elif "\\xc3\\xbc" in word:
        return word.replace("\\xc3\\xbc", "ü")
    else:
        return word
