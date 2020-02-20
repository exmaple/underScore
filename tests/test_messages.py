import pytest
from utils.messages import embedded_stats


@pytest.mark.parametrize(
    ("stats", "expected"),
    [
        ({"height": "123"}, 1),
        ({"height": "123", "weight": "456"}, 2),
        ({"height": "123", "weight": "456", "goals": "789"}, 3),
    ],
)
def test_embedded_stats(stats, expected):
    embed = embedded_stats("title", **stats)
    assert len(embed.fields) == expected
