from bs4 import BeautifulSoup
from tempfile import TemporaryFile
import logging
from ...download.get_html import download_raw_html
from utils.misc import umlaut


logger = logging.getLogger("app")


def get_matchday_results(matchday, season):
    """Scrape html for matchday results using BeautifulSoup

    Args:
        site_html(str): raw html of the website containing the matchday data

    Returns:
        dictionary containing team matchups and the corresponding score
        e.g. {0: [('Team Name', 'Score'),('Team Name', 'Score')], ... }
    """
    url = f"https://www.fussballdaten.de/bundesliga/{season[5:9]}/{matchday}"
    raw_html = download_raw_html(url)

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
