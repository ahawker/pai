"""
    conftest
    ~~~~~~~~

    High level fixtures used across all test modules.
"""

import pytest


@pytest.fixture(scope='function', params=[
    ('', '', ''),
    ('foo', 'bar', 'baz'),
    ('resource', 'relation', 'value')
])
def fake_root_node_input(request):
    """
    Fixture that yields three item tuples containing fake input to create a root :class:`~pai_lang.syntax.Node` node.
    """
    return request.param


@pytest.fixture(scope='function', params=[
    ('', ''),
    ('foo', 'bar'),
    ('resource', 'relation')
])
def fake_child_node_input(request):
    """
    Fixture that yields two item tuples containing fake input to create a child :class:`~pai_lang.syntax.Node` node.
    """
    return request.param
