from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def main():
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

    # https://www.fussballdaten.de/bundesliga/2020/14/
    driver = webdriver.Firefox()
    url = 'https://www.fussballdaten.de/bundesliga/' + season[5:9] + '/' + matchday
    driver.get(url)
    season = season.replace('/', '_')
    filename  = 'fussballdaten_' + season + '_' + matchday + '.html'
    f = open(filename, "w")
    f.write(driver.page_source)
    f.close()
    driver.close()



if __name__ == '__main__':
    main()
