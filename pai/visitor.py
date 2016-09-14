"""
    pai.visitor
    ~~~~~~~~~~~

    Module that implements the "visitor" interface defined by :mod:`~paip.parser` to implement and enforce our
    language syntax.
"""

from pai import syntax
from paip import slicer


__all__ = ['supports', 'visit']


def supports(group_size, rtl, expected_group_size=syntax.GROUP_SIZE, expected_rtl=syntax.RTL):
    """
    Check to see if the given `group_size` and `rtl` are supported by this visitor.

    :param group_size: Size of each group of tokens that will be fed into visitor
    :param rtl: Flag indicating if token groups are being returned right-to-left
    :param expected_group_size: Expected group size for this visitor
    :param expected_rtl: Expected rtl flag for this visitor
    :return: `True` if this visitor supports the specified `group_size` and `rtl` and `False` otherwise
    """
    if group_size != expected_group_size:
        return False

    if rtl != expected_rtl:
        return False

    return True


def visit(tokens, group_size, rtl, parent=None):
    """
    Consume values from given token iterable to create a :class:`~pai.syntax.Node` instance.

    :param tokens: Iterable that yields tokens to be consumed
    :param group_size: Size of each group of tokens in iterable
    :param rtl: Flag indicating if token groups are being returned right-to-left
    :param parent: A :class:`~pai.syntax.Node` instance that was created in previous visit step over this token iterable
    :return: A :class:`~pai.syntax.Node` instance
    """
    if not parent:
        return visit_root(tokens)

    return visit_child(tokens, parent)


def visit_root(tokens, n=syntax.ROOT_NODE_SIZE):
    """
    Consume values from the given token iterable to create a "root" :class:`~pai.syntax.Node` instance.

    :param tokens: Iterable that yields tokens to be consumed
    :param n: Number of tokens to consume from iterable in order to create a "root" node
    :return: A "root" :class:`~pai.syntax.Node` instance created from :func:`~pai.syntax.root`
    """
    node = visit_node(tokens, n)
    if not node:
        return None
    return syntax.root(*node)


def visit_child(tokens, parent, n=syntax.CHILD_NODE_SIZE):
    """
    Consume values from the given token iterable to create a "child" :class:`~pai.syntax.Node` instance.

    :param tokens: Iterable that yields tokens to be consumed
    :param parent: A :class:`~pai.syntax.Node` instance that was created in previous visit step for this token iterable
    :param n: Number of tokens to consume from iterable in order to create a "child" node
    :return: A "child" :class:`~pai.syntax.Node` instance created from :func:`~pai.syntax.child`
    """
    node = visit_node(tokens, n)
    if not node:
        return None
    return syntax.child(*node, parent)


def visit_node(tokens, n):
    """
    Consume `n` values from the given token iterable that will be used to create a :class:`~pai.syntax.Node` instance.

    Raises a :class:`~pai.syntax.SyntaxError` when the token iterable contains less than `n` number of items.

    :param tokens: Iterable that yields tokens to be consumed
    :param n: Number of tokens to consume from iterable in order to create the node
    :return: A :class:`~tuple` containing `n` items consumed from the token iterable, otherwise `None` if iterable
    is empty or fully exhausted
    """
    try:
        return reversed(slicer.iter_slice(tokens, n))
    except slicer.SliceIterableEmpty:
        return None
    except slicer.SliceIterableExhausted:
        raise syntax.SyntaxError('Insufficient tokens; expected {}'.format(n))
