from cStringIO import StringIO

from tonym import btree


RELATED_TREES = """\
1,5,4,,3,2,5,,,,,,,0,8
4,2,5
"""

UNRELATED_TREES = """\
1,5,4,,3,2,9,,,,,,,0,8
4,2,5
"""


def create_file_object(data):
    file_ = StringIO()
    file_.write(data)
    file_.reset()
    return file_


def test_related_trees(io):
    tree_a, tree_b = io.parse(create_file_object(RELATED_TREES))
    assert tree_a.contains(tree_b)


def test_unrelated_trees(io):
    tree_a, tree_b = io.parse(create_file_object(UNRELATED_TREES))
    assert not tree_a.contains(tree_b)


if __name__ == '__main__':
    io = btree.TreeIO()
    test_related_trees(io)
    test_unrelated_trees(io)
