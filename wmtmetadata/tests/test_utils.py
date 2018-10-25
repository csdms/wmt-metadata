import os
from wmtmetadata import top_dir
from wmtmetadata.utils import commonpath


files = [
    os.path.join(top_dir, 'foo'),
    os.path.join(top_dir, 'bar'),
    os.path.join(top_dir, 'baz'),
]

def test_commonpath():
    the_path = commonpath(files)
    assert the_path == top_dir
