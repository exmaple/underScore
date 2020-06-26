import pytest

from the_mines.process.fussballdaten.process_blurb import (
    build_matchup,
    get_team_str,
    get_glance_schedule,
    get_glance_table_stats,
    get_blurb,
)


@pytest.mark.parametrize(
    ("title", "score", "expected"),
    [
        (
            "Blah: Bayern gegen Dortmund (1.1.2001, DFB-Pokal)",
            "2:2",
            {"January 1, 2001 (DFB-Pokal)": "Bayern 2:2 Dortmund"},
        ),
        (
            "Blah: Bayern gegen Dortmund (2.2.2002, Bundesliga)",
            None,
            {"February 2, 2002 (Bundesliga)": "Bayern vs Dortmund"},
        ),
    ],
)
def test_build_matchup(title, score, expected):
    assert build_matchup(title, score) == expected


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("bayern", "fc-bayern-muenchen"),
        ("leipzig", "rb-leipzig"),
        ("mainz", "1-fsv-mainz-05"),
    ],
)
def test_get_team_str(target, expected):
    assert get_team_str(target) == expected


@pytest.mark.online
@pytest.mark.parametrize(
    ("team", "season", "expected"),
    [
        (
            "bayern",
            "2020",
            {
                "June 16, 2020 (Bundesliga)": "Bremen 0:1 Bayern",
                "June 20, 2020 (Bundesliga)": "Bayern 3:1 Freiburg",
                "June 27, 2020 (Bundesliga)": "Wolfsburg vs Bayern",
            },
        ),
        (
            "dortmund",
            "2020",
            {
                "June 17, 2020 (Bundesliga)": "Dortmund 0:2 Mainz",
                "June 20, 2020 (Bundesliga)": "RB Leipzig 0:2 Dortmund",
                "June 27, 2020 (Bundesliga)": "Dortmund vs Hoffenheim",
            },
        ),
    ],
)
def test_get_glance_schedule(team, season, expected):
    assert get_glance_schedule(team, season) == expected


@pytest.mark.online
@pytest.mark.parametrize(
    ("team", "season", "expected"),
    [
        (
            "bayern",
            "2020",
            {"title": "Bayern", "fields": {"Pos": "1", "W-T-L": "25-4-4", "Pts": "79"}},
        ),
        (
            "dortmund",
            "2020",
            {
                "title": "Dortmund",
                "fields": {"Pos": "2", "W-T-L": "21-6-6", "Pts": "69"},
            },
        ),
    ],
)
def test_get_glance_table_stats(team, season, expected):
    assert get_glance_table_stats(team, season) == expected


@pytest.mark.online
@pytest.mark.parametrize(
    ("team", "expected"),
    [
        (
            "bayern",
            {
                "title": "Bayern",
                "fields": {
                    "Pos": "1",
                    "W-T-L": "25-4-4",
                    "Pts": "79",
                    "June 16, 2020 (Bundesliga)": "Bremen 0:1 Bayern",
                    "June 20, 2020 (Bundesliga)": "Bayern 3:1 Freiburg",
                    "June 27, 2020 (Bundesliga)": "Wolfsburg vs Bayern",
                },
            },
        ),
        (
            "dortmund",
            {
                "title": "Dortmund",
                "fields": {
                    "Pos": "2",
                    "W-T-L": "21-6-6",
                    "Pts": "69",
                    "June 17, 2020 (Bundesliga)": "Dortmund 0:2 Mainz",
                    "June 20, 2020 (Bundesliga)": "RB Leipzig 0:2 Dortmund",
                    "June 27, 2020 (Bundesliga)": "Dortmund vs Hoffenheim",
                },
            },
        ),
    ],
)
def test_get_blurb(team, expected):
    assert get_blurb(team) == expected
