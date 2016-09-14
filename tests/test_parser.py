"""
    test_parser
    ~~~~~~~~~~~

    Tests for the :mod:`~pai.parser` module.
"""

import pytest

from pai import parser


@pytest.fixture(scope='function')
def single_token_ordered_visitor():
    """
    Fixture that yields an object that conforms to the "visitor" interface and visits/consumes tokens and returns
    them back, one by own, in the order that they were read.
    """
    class Visitor:
        def supports(self, group_size, rtl):
            return True

        def visit(self, tokens, group_size, rtl, parent=None):
            return next(tokens, None)

    return Visitor()


def is_root_node(node):
    """
    Return `True` if the given node is a "root" node, `False` otherwise.
    """
    if not node:
        return False
    return node.is_root is True and node.is_child is False


def is_child_node(node):
    """
    Return `True` if the given node is a "child" node, `False` otherwise.
    """
    if not node:
        return False
    return node.is_child is True and node.is_root is False


@pytest.fixture(scope='module', params=[
    'a:b:c',
    'd:e:f',
    'foo:bar:baz',
    'node:edge:property'
])
def root_node_only_token_stream(request):
    """
    Fixture that yields strings that will generate a token stream that creates a single root node.
    """
    return request.param


@pytest.fixture(scope='module', params=[
    'a:b',
    'c:d',
    'foo:bar',
    'node1:edge1'
])
def root_and_child_node_token_stream(request, root_node_only_token_stream):
    """
    Fixture that yields strings that will generate a token stream that creates one root node and one child node.
    """
    return ':'.join((request.param, root_node_only_token_stream))


@pytest.fixture(scope='module', params=[
    'w:x',
    'y:z',
    'bar:baz',
    'node2:edge2'
])
def root_and_two_child_nodes_token_stream(request, root_and_child_node_token_stream):
    """
    Fixture that yields strings that will generate a token stream that creates one root and two child nodes.
    """
    return ':'.join((request.param, root_and_child_node_token_stream))


def test_parse_returns_one_root_node_per_syntax(root_node_only_token_stream):
    """
    Assert that :func:`~pai.parser.parse` returns a single root node per :mod:`~pai.syntax` specification.
    """
    nodes = parser.parse(root_node_only_token_stream)
    assert len(nodes) == 1
    assert is_root_node(nodes[0])


def test_parse_gen_yields_one_root_node_per_syntax(root_node_only_token_stream):
    """
    Assert that :func:`~pai.parser.parse` yields a single root node per :mod:`~pai.syntax` specification.
    """
    nodes = list(parser.parse_gen(root_node_only_token_stream))
    assert len(nodes) == 1
    assert is_root_node(nodes[0])


def test_parse_returns_root_and_child_node_per_syntax(root_and_child_node_token_stream):
    """
    Assert that :func:`~pai.parser.parse` returns a root and child node per :mod:`~pai.syntax` specification.
    """
    nodes = parser.parse(root_and_child_node_token_stream)
    assert len(nodes) == 2
    assert is_root_node(nodes[0])
    assert is_child_node(nodes[1])


def test_parse_gen_yields_root_and_child_node_per_syntax(root_and_child_node_token_stream):
    """
    Assert that :func:`~pai.parser.parse_gen` returns a root and child node per :mod:`~pai.syntax` specification.
    """
    nodes = list(parser.parse_gen(root_and_child_node_token_stream))
    assert len(nodes) == 2
    assert is_root_node(nodes[0])
    assert is_child_node(nodes[1])


def test_parse_returns_root_and_two_child_nodes_per_syntax(root_and_two_child_nodes_token_stream):
    """
    Assert that :func:`~pai.parser.parse` returns a root and two child nodes per :mod:`~pai.syntax` specification.
    """
    nodes = parser.parse(root_and_two_child_nodes_token_stream)
    assert len(nodes) == 3
    assert is_root_node(nodes[0])
    assert is_child_node(nodes[1])
    assert is_child_node(nodes[2])


def test_parse_gen_yields_root_and_two_child_nodes_per_syntax(root_and_two_child_nodes_token_stream):
    """
    Assert that :func:`~pai.parser.parse_gen` returns a root and two child nodes per :mod:`~pai.syntax` specification.
    """
    nodes = list(parser.parse_gen(root_and_two_child_nodes_token_stream))
    assert len(nodes) == 3
    assert is_root_node(nodes[0])
    assert is_child_node(nodes[1])
    assert is_child_node(nodes[2])
