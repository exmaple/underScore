import re
import logging

from bs4 import BeautifulSoup
from datetime import date
from tempfile import TemporaryFile
from utils.misc import umlaut
from ...download.get_html import download_raw_html

logger = logging.getLogger("app")

def live_match(match, matchup_score, matchdays):
    matchdate = date.today()
    matchdate = matchdate.strftime("%d.%m.%Y")

    match = umlaut(match.get_text())

    team_re = re.compile("\)([^|]*)\(")
    match, = team_re.findall(match)
    no_digits = re.compile("\D+")
    match = no_digits.findall(match)
    while ":" in match:
        match.remove(":")
    matchup = match
    for team in matchup:
        matchup_score.append((team, "LIVE"))

    matchdays[matchdate].append(matchup_score)


def future_match(match, match_details, matchup_score, matchdays, matchdate, date_re):
    try:
        match_details, = match.find_all(
            "a", attrs={"title": re.compile("Vorschau:*")}
        )
    except ValueError:
        return False

    team_re = re.compile("\)([^|]*)\(")
    no_digits = re.compile("\D+")

    matchdate, = date_re.findall(match_details["title"])
    # matchdate = matchdate[0]

    match = umlaut(match.get_text())
    # (16.)Düsseldorf15:30Dortmund(2.)- w -17,50X5,2521,36

    matchup, = team_re.findall(match)
    # ['Düsseldorf15:30Dortmund']

    matchup = no_digits.findall(matchup)
    # ['Düsseldorf', ':', 'Dortmund']

    while ":" in matchup:
        matchup.remove(":")
    # ['Düsseldorf', 'Dortmund']


    # add matchup to dict without score
    for team in matchup:
        matchup_score.append((team, "tbd"))

    matchdays[matchdate].append(matchup_score)
    return True

def past_match(match, match_details, matchup_score, matchdays, score_list, matchdate, date_re):

    try:
        match_details, = match.find_all(
            "a", attrs={"title": re.compile("Spieldetails:*")}
        )
    except ValueError:
        return False


    matchdate, = date_re.findall(match_details["title"])
    # matchdate = matchdate[0]
    match = re.sub("\(\d+.\)", "", match.get_text())
    match = umlaut(match)

    team_re = re.compile("([\D]+)")
    matchup = team_re.findall(match)

    while ":" in matchup:
        matchup.remove(":")

    # add matchup to dict with score
    for team in matchup:
        if len(score_list[0]) == 0:
            del score_list[0]
        matchup_score.append((team, score_list[0].pop(0)))

    matchdays[matchdate].append(matchup_score)
    return True

def create_initial_dict(dates, date_re):
    """ Create dictionary keys
        Each key is a unique date on which matches occur

    Args:
        dates(bs4.element.ResultSet): a soup in which match dates are contained
        date_re(re.Pattern): regex pattern to sift through soup and capture match dates

    Returns:
        dictionary where each key is a date on which matches are played on the specified matchday
        with an empty list as the keys' value.
        eg. {'14.06.2020': [], '12.06.2020': [], '13.06.2020': []}
    """
    matchdays = {}
    for day in dates:
        matchdate = date_re.findall(day.get_text())[0]
        matchdays[matchdate] = []

    return matchdays

def get_initial_data(soup):
    """Retrieve initial soup

    Args:
        soup(BeautifulSoup object): soupified html

    Returns:
        dates: soup containing match dates for the specified matchday
        matches: soup containing info on matches played on the specified matchday (except score)
        score_list: soup containing info on scores of the matches

    """
    dates = soup.find_all("div", attrs={"class": "datum-row"})
    matches = soup.find_all("div", attrs={"class": "spiele-row detils"})
    score_tag = soup.find_all("span", attrs={"id": re.compile("\d\d\d\d\d")})
    score_list = [score.get_text().split(":") for score in score_tag]

    return dates, matches, score_list

def process_results(matchday, season):
    """Scrape html for matchday results using BeautifulSoup

    Args:
        matchday(str): number representing the match day e.g. '13'
        season(str): number representing the season e.g. '2019/2020'

    Returns:
        dictionary containing team matchups and the corresponding score
        e.g. {'14.06.2020': [[('Mainz', 'tbd'), ('Augsburg', 'tbd')], [('Schalke', 'tbd'), ('Leverkusen', 'tbd')]], '12.06.2020': [[('Hoffenheim', '0'), ('RB Leipzig', '2')]], '13.06.2020': [[('Wolfsburg', '2'), ('Freiburg', '2')], [('Düsseldorf', '0'), ('Dortmund', '1')], [('Hertha BSC', '1'), ('Frankfurt', '4')], [('Köln', '1'), ('Union Berlin', '2')], [('Paderborn', '1'), ('Bremen', '5')], [('Bayern', '2'), ("M'gladbach", '1')]]}
    """

    url = f"https://www.fussballdaten.de/bundesliga/{season[5:9]}/{matchday}"
    raw_html = download_raw_html(url)
    date_re = re.compile("\d+.\d+.\d+")

    with TemporaryFile("w+") as tmp:
        tmp.write(raw_html)
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        dates, matches, score_list = get_initial_data(soup)
        matchdays = create_initial_dict(dates, date_re)

        """ Add matches to dictionary according to date match was played
        """
        matchup = []
        for match in matches:
            match_details = []
            matchup_score = []
            matchdate = ""  # dd.mm.yyyy

            # if match has been played
            played = past_match(match, match_details, matchup_score, matchdays, score_list, matchdate, date_re)

            # if the match has not yet been played
            if played == False:
                played = future_match(match, match_details, matchup_score, matchdays, matchdate, date_re)

            # if the match is live
            if played == False:
                live_match(match, matchup_score, matchdays)



    return matchdays
