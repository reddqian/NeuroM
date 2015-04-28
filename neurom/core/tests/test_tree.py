from nose import tools as nt
from neurom.core.tree import Tree
from neurom.core.tree import iter_preorder
from neurom.core.tree import iter_postorder
from neurom.core.tree import iter_upstream
from neurom.core.tree import iter_segment
from neurom.core.tree import iter_leaf
from neurom.core.tree import iter_forking_point
from neurom.core.tree import val_iter


REF_TREE = Tree(0)
REF_TREE.add_child(Tree(11))
REF_TREE.add_child(Tree(12))
REF_TREE.children[0].add_child(Tree(111))
REF_TREE.children[0].add_child(Tree(112))
REF_TREE.children[1].add_child(Tree(121))
REF_TREE.children[1].add_child(Tree(122))
REF_TREE.children[1].children[0].add_child(Tree(1211))
REF_TREE.children[1].children[0].children[0].add_child(Tree(12111))
REF_TREE.children[1].children[0].children[0].add_child(Tree(12112))


def test_instantiate_tree():
    t = Tree('hello')
    nt.ok_(t.parent is None)
    nt.ok_(t.value == 'hello')
    nt.ok_(len(t.children) == 0)


def test_children():
    nt.ok_(REF_TREE.children[0].value == 11)
    nt.ok_(REF_TREE.children[1].value == 12)
    nt.ok_(REF_TREE.children[0].children[0].value == 111)
    nt.ok_(REF_TREE.children[0].children[1].value == 112)
    nt.ok_(REF_TREE.children[1].children[0].value == 121)
    nt.ok_(REF_TREE.children[1].children[1].value == 122)


def test_add_child():
    t = Tree(0)
    t.add_child(Tree(11))
    t.add_child(Tree(22))
    nt.ok_(t.value == 0)
    nt.ok_(len(t.children) == 2)
    nt.ok_([i.value for i in t.children] == [11, 22])


def test_parent():
    t = Tree(0)
    for i in xrange(10):
        t.add_child(Tree(i))

    nt.ok_(len(t.children) == 10)

    for c in t.children:
        nt.ok_(c.parent is t)


def test_preorder_iteration():
    nt.ok_(list(val_iter(iter_preorder(REF_TREE))) ==
           [0, 11, 111, 112, 12, 121, 1211, 12111, 12112, 122])
    nt.ok_(list(val_iter(iter_preorder(REF_TREE.children[0]))) == [11, 111, 112])
    nt.ok_(list(val_iter(iter_preorder(REF_TREE.children[1]))) ==
           [12, 121, 1211, 12111, 12112, 122])


def test_postorder_iteration():
    nt.ok_(list(val_iter(iter_postorder(REF_TREE))) ==
           [111, 112, 11, 12111, 12112, 1211, 121, 122, 12, 0])
    nt.ok_(list(val_iter(iter_postorder(REF_TREE.children[0]))) == [111, 112, 11])
    nt.ok_(list(val_iter(iter_postorder(REF_TREE.children[1]))) ==
           [12111, 12112, 1211, 121, 122, 12])


def test_upstream_iteration():

    nt.ok_(list(val_iter(iter_upstream(REF_TREE))) == [0])
    nt.ok_(list(val_iter(iter_upstream(REF_TREE.children[0]))) == [11, 0])
    nt.ok_(list(val_iter(iter_upstream(REF_TREE.children[0].children[0]))) ==
           [111, 11, 0])
    nt.ok_(list(val_iter(iter_upstream(REF_TREE.children[0].children[1]))) ==
           [112, 11, 0])


    nt.ok_(list(val_iter(iter_upstream(REF_TREE.children[1]))) == [12, 0])
    nt.ok_(list(val_iter(iter_upstream(REF_TREE.children[1].children[0]))) ==
           [121, 12, 0])
    nt.ok_(list(val_iter(iter_upstream(REF_TREE.children[1].children[1]))) ==
           [122, 12, 0])


def test_segment_iteration():
    nt.ok_(list(iter_segment(REF_TREE)),
           [(0, 11),(11, 111),(11, 112),
            (0, 12),(12, 121),(12, 122)])
    nt.ok_(list(iter_segment(REF_TREE.children[0])),
           [(0, 11), (11, 111),(11, 112)])
    nt.ok_(list(iter_segment(REF_TREE.children[0].children[0])), [(11, 111)])
    nt.ok_(list(iter_segment(REF_TREE.children[0].children[1])), [(11, 112)])
    nt.ok_(list(iter_segment(REF_TREE.children[1])),
           [(0, 12), (12, 121),(12, 122)])
    nt.ok_(list(iter_segment(REF_TREE.children[1].children[0])), [(12, 121)])
    nt.ok_(list(iter_segment(REF_TREE.children[1].children[1])), [(12, 122)])


def test_leaf_iteration():
    nt.ok_(list(val_iter(iter_leaf(REF_TREE))) == [111, 112, 12111, 12112, 122])
    nt.ok_(list(val_iter(iter_leaf(REF_TREE.children[0]))) == [111, 112])
    nt.ok_(list(val_iter(iter_leaf(REF_TREE.children[1]))) == [12111, 12112, 122])
    nt.ok_(list(val_iter(iter_leaf(REF_TREE.children[0].children[0]))) == [111])
    nt.ok_(list(val_iter(iter_leaf(REF_TREE.children[0].children[1]))) == [112])
    nt.ok_(list(val_iter(iter_leaf(REF_TREE.children[1].children[0]))) == [12111, 12112])
    nt.ok_(list(val_iter(iter_leaf(REF_TREE.children[1].children[1]))) == [122])


def test_iter_forking_point():
    nt.ok_([n.value for n in iter_forking_point(REF_TREE)] ==
           [0, 11, 12, 1211])


def test_valiter_forking_point():
    nt.ok_(list(val_iter(iter_forking_point(REF_TREE))) ==
           [0, 11, 12, 1211])