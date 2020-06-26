import pytest

from the_mines.process.fussballdaten.process_matchday import (
    live_match,
    future_match,
    past_match,
    create_initial_dict,
    get_initial_data,
    process_results,
)


def test_live_match(match, matchup_score, matchdays):
    assert True
