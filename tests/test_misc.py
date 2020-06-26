import pytest
import re
from utils.misc import (
    umlaut,
    unumlaut,
    format_date,
    open_default_html,
    get_default_matchday,
    get_default_season,
)


@pytest.mark.parametrize(
    ("word", "expected"),
    [("f\\xc3\\xb6\\xc3\\xb6", "föö"), ("bar", "bar"), ("f\\xc3\\xbctbol", "fütbol"),],
)
def test_umlaut(word, expected):
    assert umlaut(word) == expected


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("föö", "foo"),
        ("bär", "bar"),
        ("fütbol", "futbol"),
        ("áēïōü", "aeiou"),
        ("test", "test"),
    ],
)
def test_unumlaut(word, expected):
    assert unumlaut(word) == expected


@pytest.mark.parametrize(
    ("date", "expected"),
    [("10.10.2010", "October 10, 2010"), ("1.2.2012", "February 1, 2012"),],
)
def test_format_date(date, expected):
    assert format_date(date) == expected


@pytest.mark.online
@pytest.mark.parametrize(
    ("pattern"),
    [("Die aktuelle Bundesliga 20\d\d/20\d\d - Der \d*\. Spieltag - Fussballdaten")],
)
def test_open_default_html(pattern):
    assert re.match(pattern, open_default_html())


@pytest.mark.online
@pytest.mark.parametrize(("earliest", "latest"), [(1, 34)])
def test_get_default_matchday(earliest, latest):
    result = int(get_default_matchday())
    assert result >= earliest and result <= latest


@pytest.mark.online
@pytest.mark.parametrize(("pattern"), [("20\d\d")])
def test_get_default_season(pattern):
    assert re.match(pattern, get_default_season())
