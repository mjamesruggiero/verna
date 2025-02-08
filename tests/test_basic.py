from context import verna
from verna import core

def test_count_files_by_extension():
    test_dir = "/Users/michael/code/mr/verna"
    sut = core.count_files_by_extension(test_dir)
    assert sut[".py"] == 4
