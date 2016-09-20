"""
    test_visitor
    ~~~~~~~~~~~~

    Tests for the :mod:`~pai_lang.visitor` module.
"""

import pytest

from pai_lang import syntax, visitor


@pytest.fixture(scope='module', params=[
    (0, 1),
    (1, 2),
    (0, 3),
    (2, 4),
    (10, 2)
])
def group_size_mismatching_pairs(request):
    """
    Fixture that yields two item tuples representing mismatching group sizes.
    """
    return request.param


@pytest.fixture(scope='module', params=[
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (10, 10)
])
def group_size_matching_pairs(request):
    """
    Fixture that yields two item tuples representing matching group sizes.
    """
    return request.param


@pytest.fixture(scope='module', params=[
    (True, False),
    (False, True)
])
def rtl_mismatching_pairs(request):
    """
    Fixture that yields two item tuples representing mismatching rtl values.
    """
    return request.param


@pytest.fixture(scope='module', params=[
    (True, True),
    (False, False)
])
def rtl_matching_pairs(request):
    """
    Fixture that yields two item tuples representing matching rtl values.
    """
    return request.param


@pytest.fixture(scope='function')
def valid_visit_root_node_params(fake_root_node_input):
    """
    Fixture that yields a tuple of tokens, group_size, and rtl values that can be passed into
    :func:`~pai_lang.visitor.visit` to create a valid root :class:`~pai_lang.syntax.Node` node.
    """
    return fake_root_node_input, syntax.GROUP_SIZE, syntax.RTL


@pytest.fixture(scope='function')
def valid_visit_child_node_params(fake_child_node_input):
    """
    Fixture that yields a tuple of tokens, group_size, and rtl values that can be passed into
    :func:`~pai_lang.visitor.visit` to create a valid child :class:`~pai_lang.syntax.Node` node.
    """
    return fake_child_node_input, syntax.GROUP_SIZE, syntax.RTL


@pytest.fixture(scope='function')
def insufficient_tokens_visit_root_node_params(fake_root_node_input):
    """
    Fixture that yields a tuple of tokens, group_size, and rtl values that can be passed into
    :func:`~pai_lang.visitor.visit` that does not contain enough tokens to create a valid
    root :class:`~pai_lang.syntax.Node` node.
    """
    return fake_root_node_input[:-1], syntax.GROUP_SIZE, syntax.RTL


@pytest.fixture(scope='function')
def insufficient_tokens_visit_child_node_params(fake_child_node_input):
    """
    Fixture that yields a tuple of tokens, group_size, and rtl values that can be passed into
    :func:`~pai_lang.visitor.visit` that does not contain enough tokens to create a valid
    child :class:`~pai_lang.syntax.Node` node.
    """
    return fake_child_node_input[:-1], syntax.GROUP_SIZE, syntax.RTL


@pytest.fixture(scope='module')
def empty_tokens_visit_params():
    """
    Fixture that yields a tuple of tokens, group_size, and rtl values that can be passed into
    :func:`~pai_lang.visitor.visit` that does not have any tokens to create a valid :class:`~pai_lang.syntax.Node` node.
    """
    return [], syntax.GROUP_SIZE, syntax.RTL


def test_support_returns_false_on_group_size_mismatch(group_size_mismatching_pairs):
    """
    Assert that :func:`~pai_lang.visitor.supports` returns `False` when given a `group_size` and `expected_group_size`
    that are not equal.
    """
    group_size, expected_group_size = group_size_mismatching_pairs
    assert visitor.supports(group_size, syntax.RTL, expected_group_size) is False


def test_support_returns_false_on_rtl_mismatch(group_size_matching_pairs, rtl_mismatching_pairs):
    """
    Assert that :func:`~pai_lang.visitor.supports` returns `False` when given a `rtl` and `expected_rtl`
    that are not equal.
    """
    group_size, expected_group_size = group_size_matching_pairs
    rtl, expected_rtl = rtl_mismatching_pairs
    assert visitor.supports(group_size, rtl, expected_group_size, expected_rtl) is False


def test_support_returns_true_on_group_size_match(group_size_matching_pairs):
    """
    Assert that :func:`~pai_lang.visitor.supports` returns `True` when given a `group_size` and `expected_group_size`
    that are equal.
    """
    group_size, expected_group_size = group_size_matching_pairs
    assert visitor.supports(group_size, syntax.RTL, expected_group_size) is True


def test_support_returns_true_on_rtl_match(group_size_matching_pairs, rtl_matching_pairs):
    """
    Assert that :func:`~pai_lang.visitor.supports` returns `True` when given a `rtl` and `expected_rtl`
    that are equal.
    """
    group_size, expected_group_size = group_size_matching_pairs
    rtl, expected_rtl = rtl_matching_pairs
    assert visitor.supports(group_size, rtl, expected_group_size, expected_rtl) is True


def test_visit_returns_root_node_when_not_given_parent(valid_visit_root_node_params):
    """
    Assert that :func:`~pai_lang.visitor.visit` returns a root :class:`~pai_lang.syntax.Node` node when given input
    without a parent value.
    """
    root = visitor.visit(*valid_visit_root_node_params, parent=None)
    assert root.is_root is True
    assert root.is_child is False


def test_visit_returns_child_node_when_given_parent(valid_visit_root_node_params, valid_visit_child_node_params):
    """
    Assert that :func:`~pai_lang.visitor.visit` returns a child :class:`~pai_lang.syntax.Node` node when given input
    with a parent value to another node.
    """
    root = visitor.visit(*valid_visit_root_node_params, parent=None)
    child = visitor.visit(*valid_visit_child_node_params, parent=root)
    assert child.is_child is True
    assert child.is_root is False


def test_visit_raises_syntax_error_on_missing_tokens_for_root_node(insufficient_tokens_visit_root_node_params):
    """
    Assert that :func:`~pai_lang.visitor.visit` raises a :class:`~pai_lang.syntax.SyntaxError` when given a token stream that
    does not have a sufficient number of items to create a root :class:`~pai_lang.syntax.Node` node.
    """
    with pytest.raises(syntax.SyntaxError):
        visitor.visit(*insufficient_tokens_visit_root_node_params, parent=None)


def test_visit_raises_syntax_error_on_missing_tokens_for_child_node(valid_visit_root_node_params,
                                                                    insufficient_tokens_visit_child_node_params):
    """
    Assert that :func:`~pai_lang.visitor.visit` raises a :class:`~pai_lang.syntax.SyntaxError` when given a token stream that
    does not have a sufficient number of items to create a root :class:`~pai_lang.syntax.Node` node.
    """
    root = visitor.visit(*valid_visit_root_node_params, parent=None)
    with pytest.raises(syntax.SyntaxError):
        visitor.visit(*insufficient_tokens_visit_child_node_params, parent=root)


def test_visit_returns_none_root_node_on_empty_tokens_iterable(empty_tokens_visit_params):
    """
    Assert that :func:`~pai_lang.visitor.visit` returns `None` when given an empty token iterable instead of a root
    :class:`~pai_lang.syntax.Node` node.
    """
    assert visitor.visit(*empty_tokens_visit_params, parent=None) is None


def test_visit_returns_none_child_node_on_empty_tokens_iterable(valid_visit_root_node_params,
                                                                empty_tokens_visit_params):
    """
    Assert that :func:`~pai_lang.visitor.visit` returns `None` when given an empty token iterable instead of a root
    :class:`~pai_lang.syntax.Node` node.
    """
    root = visitor.visit(*valid_visit_root_node_params, parent=None)
    assert visitor.visit(*empty_tokens_visit_params, parent=root) is None
