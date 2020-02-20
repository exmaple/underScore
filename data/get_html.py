from argparse import ArgumentParser
import requests

def get_html():
    parser = ArgumentParser()
    parser.add_argument(
        "--matchday",
        action="store",
        required=True,
        help="ex. 8",
    )
    parser.add_argument(
        "--season",
        action="store",
        required=True,
        help="ex. 2019/2020",
    )
    args = parser.parse_args()

    matchday = f"{args.matchday}"
    season = f"{args.season}"


    url = 'https://www.fussballdaten.de/bundesliga/' + season[5:9] + '/' + matchday

    page_source = requests.get(url)
    season = season.replace('/', '_')
    filename  = 'fussballdaten_' + season + '_' + matchday + '.html'
    f = open(filename, "w")
    f.write(str(page_source.content))
    f.close()

def main():
    get_html()





if __name__ == '__main__':
    main()
