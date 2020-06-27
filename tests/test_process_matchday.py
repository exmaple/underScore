import pytest

from the_mines.process.fussballdaten.process_matchday import (
    live_match,
    future_match,
    past_match,
    create_initial_dict,
    get_initial_data,
    process_results,
)


@pytest.mark.online
@pytest.mark.parametrize(
    ("matchday", "season", "expected"),
    [
        (
            "34",
            "2020",
            [
                [("Frankfurt", "3"), ("Paderborn", "2")],
                [("Bremen", "6"), ("Köln", "1")],
                [("Freiburg", "4"), ("Schalke", "0")],
                [("Augsburg", "1"), ("RB Leipzig", "2")],
                [("Union Berlin", "3"), ("Düsseldorf", "0")],
                [("Dortmund", "0"), ("Hoffenheim", "4")],
                [("Leverkusen", "1"), ("Mainz", "0")],
                [("M\\'gladbach", "2"), ("Hertha BSC", "1")],
                [("Wolfsburg", "0"), ("Bayern", "4")],
            ],
        )
    ],
)
def test_process_results(matchday, season, expected):
    results = process_results(matchday, season)["27.06.2020"]
    for match in expected:
        assert match in results
