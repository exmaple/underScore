import re
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from tempfile import TemporaryFile

from ...download.get_html import download_html, download_default_html

def get_default_matchday(matchday_or_season):
    raw_html = download_default_html()
    with TemporaryFile("w+") as tmp:
        tmp.write(raw_html)
        tmp.seek(0)
        soup = BeautifulSoup(tmp, "html.parser")

        title = soup.title.text
        if matchday_or_season == 'matchday':
            ind = title.index('.')
            matchday = title[ind-2:ind]
        elif matchday_or_season == 'season':
            ind = title.index('/')
            matchday = title[ind-4:ind+5]

    return matchday.strip()


def get_matchday_results(matchday, season):
    raw_html = download_html(matchday, season)
    return process_results(raw_html)


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
        soup = BeautifulSoup(tmp, 'html.parser')
        matches = {}

        ''' Example team_list
        ['Freiburg', "M'gladbach", 'RB Leipzig', 'Paderborn', 'Leverkusen', 'Bayern', 'Frankfurt', 'Mainz', 'Düsseldorf', 'Hoffenheim', 'Dortmund', 'Hertha BSC', 'Bremen', 'Wolfsburg', 'Union Berlin', 'Schalke', 'Augsburg', 'Köln']
        '''
        all_teams = soup.find_all('a', attrs={'title': re.compile('Details zu*')})
        team_list = []
        for team in all_teams:
            team = team.get_text()
            team = re.sub('\(.*\)', '', team)
            team = umlaut(team)
            team_list.append(team)

        ''' Example full_matchup_list
        [['Freiburg', "M'gladbach"], ['RB Leipzig', 'Paderborn'], ['Leverkusen', 'Bayern'], ['Frankfurt', 'Mainz'], ['Düsseldorf', 'Hoffenheim'], ['Dortmund', 'Hertha BSC'], ['Bremen', 'Wolfsburg'], ['Union Berlin', 'Schalke']]
        '''
        matchup_list = []
        full_matchup_list = []
        for i in range(len(team_list)):
            matchup_list.append(team_list.pop(0))
            if (len(team_list) % 2 == 0):
                full_matchup_list.append(matchup_list)
                matchup_list = []

        ''' Example score_list
        [['1', '0'], ['1', '1'], ['2', '4'], ['0', '2'], ['2', '2'], ['1', '0'], ['0', '1'], ['1', '1'], ['1', '1']]
        '''
        score_tag = soup.find_all('span', attrs={'id': re.compile('\d\d\d\d\d')})
        score_list = [score.get_text().split(':') for score in score_tag]
        if len(score_list) == 0:
            score_list = [['tbd', 'tbd'] for x in full_matchup_list]

        ''' Example matches dictionary
        {0: [('Freiburg', '1'), ("M'gladbach", '0')], 1: [('RB Leipzig', '1'), ('Paderborn', '1')], 2: [('Leverkusen', '2'), ('Bayern', '4')], 3: [('Frankfurt', '0'), ('Mainz', '2')], 4: [('Düsseldorf', '2'), ('Hoffenheim', '2')], 5: [('Dortmund', '1'), ('Hertha BSC', '0')], 6: [('Bremen', '0'), ('Wolfsburg', '1')], 7: [('Union Berlin', '1'), ('Schalke', '1')], 8: [('Augsburg', '1'), ('Köln', '1')]}
        '''

        i = 0
        for i in range(len(score_list)):
            x = [(full_matchup_list[i][0], score_list[i][0]),(full_matchup_list[i][1], score_list[i][1])]
            print(x)
            matches[i] = x

    print(matches)
    return matches


def umlaut(word_with_umlaut):
    """Insert accented chars where applicable

    Args:
        word_with_umlaut(str): a word containing an umlaut
    Returns:
        word with actual umlaut
    """
    if "\\xc3\\xb6" in word_with_umlaut:
        word_with_umlaut = word_with_umlaut.replace("\\xc3\\xb6", "ö")
    elif "\\xc3\\xbc" in word_with_umlaut:
        word_with_umlaut = word_with_umlaut.replace("\\xc3\\xbc", "ü")
    return word_with_umlaut
