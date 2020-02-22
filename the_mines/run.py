from get_html import get_html
from scrape_html import fussballdatenpunktde_matchday_results

html_file = get_html()

fussballdatenpunktde_matchday_results('data/'+html_file)
