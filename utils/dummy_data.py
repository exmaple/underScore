from random import choice, randrange


def get_dummy_data(player_name):
    """Creates a series of randomized statistics

    Returns:
        series of ints and strings
    """
    return {
        "title": f"{player_name} Stats",
        "fields": {
            "height": randrange(150, 200),
            "weight": randrange(50, 110),
            "position": choice(["GK", "CB", "CM", "ST"]),
            "gp": randrange(1, 50),
            "goals": randrange(50),
            "assists": randrange(50),
        }
    }
