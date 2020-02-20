from bs4 import BeautifulSoup
from argparse import ArgumentParser

def fussballdatenpunktde(site_html):
    '''
    fussballdaten.de
    view-source:https://www.fussballdaten.de/bundesliga/2020/12/
    '''
    with open(f"{site_html.html}") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    game_count = 0
    game_dict = {}
    a_tag = soup('a')
    for game_details in a_tag:

        if 'id' in game_details.attrs and 'class' in game_details.attrs:
            teams_list = []
            teams_string = game_details.get('title')
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
                counter +=1
            if teams_string_list[2] == 'gegen' and len(teams_string_list) == 6:
                # 1/1
                teams_list.append((teams_string_list[1],score1))
                teams_list.append((teams_string_list[3],score2))
            elif teams_string_list[3] == 'gegen' and len(teams_string_list) == 7:
                # 2/1
                team1 = teams_string_list[1] + " " + teams_string_list[2]
                team2 = teams_string_list[4]
                teams_list.append((team1,score1))
                teams_list.append((team2,score2))
            elif teams_string_list[2] == 'gegen' and len(teams_string_list) == 7:
                # 1/2
                team1 = teams_string_list[1]
                team2 = teams_string_list[3] + " " + teams_string_list[4]
                teams_list.append((team1, score1))
                teams_list.append((team2, score2))
            elif teams_string_list[3] == 'gegen' and len(teams_string_list) == 8:
                # 2/2
                team1 = teams_string_list[1] + " " + teams_string_list[2]
                team2 = teams_string_list[4] + " " + teams_string_list[5]
                teams_list.append((team1, score1))
                teams_list.append((team2, score2))

            game_dict[game_count] = teams_list
            game_count += 1
    print(game_dict)



def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--html",
        action="store",
        required=True,
        help="Raw HTML (ex. fussballdaten_matchday6.html)",
    )
    args = parser.parse_args()

    #bundesliadotcom()
    fussballdatenpunktde(args)


if __name__ == '__main__':
    main()
