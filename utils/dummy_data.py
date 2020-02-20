from random import choice, randrange


def get_dummy_data():
    height = randrange(150, 200)
    weight = randrange(50, 110)
    position = choice(["GK", "CB", "CM", "ST"])
    gp = randrange(1, 50)
    goals = randrange(50)
    assists = randrange(50)
    return height, weight, position, gp, goals, assists
