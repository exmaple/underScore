from argparse import ArgumentParser

from get_html import get_html
from scrape_html import fussballdatenpunktde_matchday_results

parser = ArgumentParser()

parser.add_argument(
    "--matchday", action="store", required=True, help="ex. 8",
)
parser.add_argument(
    "--season", action="store", required=True, help="ex. 2019/2020",
)
args = parser.parse_args()


'''
Get data
'''
html_file = get_html(args.matchday, args.season)

fussballdatenpunktde_matchday_results("data/" + html_file)
