from argparse import ArgumentParser

from .get_html import get_matchday_html
from .scrape_html import fussballdatenpunktde_matchday_results


def extract_matchday_results(matchday, season):

    html_file = get_matchday_html(matchday, season)

    matchday_results = fussballdatenpunktde_matchday_results("the_mines/data/" + html_file)

    return matchday_results
