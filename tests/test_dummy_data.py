from utils.dummy_data import get_dummy_data


def test_get_dummy_data():
    result_count = 0
    for result in get_dummy_data():
        result_count += 1
        if isinstance(result, int):
            assert result >= 0
        elif isinstance(result, str):
            assert len(result) == 2

    assert result_count == 6
