import pytest
from tempfile import TemporaryFile
from bs4 import BeautifulSoup

from utils.table_handler import (
    tables_from_soup,
    get_table,
    find_team_in_table,
    extract_full_table_stats,
)
from the_mines.download.get_html import download_raw_html


def get_soup(url="https://www.fussballdaten.de/bundesliga/tabelle/2019"):
    with TemporaryFile("w+") as tmp:
        tmp.write(download_raw_html(url))
        tmp.seek(0)
        return BeautifulSoup(tmp, "html.parser")


@pytest.mark.online
@pytest.mark.parametrize("expected", [(4)])
def test_tables_from_soup(expected):
    assert len(tables_from_soup(get_soup())) == expected


@pytest.mark.online
@pytest.mark.parametrize(
    ("full", "form", "home", "away", "expected"),
    [
        (True, False, False, False, 19),
        (False, True, False, False, 4),
        (False, False, True, False, 4),
        (False, False, False, True, 4),
    ],
)
def test_get_table(full, form, home, away, expected):
    assert (
        len(
            get_table(
                tables_from_soup(get_soup()), full=full, form=form, home=home, away=away
            )
        )
        == expected
    )


@pytest.mark.online
@pytest.mark.parametrize(
    ("team", "table", "expected"),
    [("bayern", get_table(tables_from_soup(get_soup()), full=True), 10)],
)
def test_find_team_in_table(team, table, expected):
    assert len(find_team_in_table(team, table)) == expected


@pytest.mark.online
@pytest.mark.parametrize(
    ("row", "expected"),
    [
        (
            find_team_in_table(
                "bayern", get_table(tables_from_soup(get_soup()), full=True)
            ),
            ("1", "Bayern", "34", "24", "6", "4", "88:32", "56", "78"),
        )
    ],
)
def test_extract_full_table_stats(row, expected):
    assert extract_full_table_stats(row) == expected
