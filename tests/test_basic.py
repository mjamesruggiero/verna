from context import verna
from verna import core
import pytest
import datetime
from pathlib import Path


# TODO fix this brittle test
def test_count_files_by_extension():
    test_dir = "/Users/michaelruggiero/code/mr/verna"
    sut = core.count_files_by_extension(test_dir)
    assert sut[".py"] == 4


def test_can_generate_datestring():
    d = datetime.datetime(1967, 9, 30)
    sut = core.canonical_date(d)
    assert sut == "1967_09_30"


def test_bad_datetime_throws():
    d = "NOT A DATETIME"
    with pytest.raises(AttributeError, match=r".*not a valid datetime*"):
        core.canonical_date(d)


def test_can_build_new_filepath():
    label = "fun with kids"
    dt = datetime.datetime(1969, 4, 21)
    base_dir = "/Users/davidlynch"
    sut = core.mk_filepath(base_dir, label, dt)
    assert sut == Path("/Users/davidlynch/1969_04_21_fun_with_kids")


def test_snake_case():
    expected = "this_isnt_a_problem"
    sut = core.snake_case("This Isn't A-Problem")
    assert sut == expected
