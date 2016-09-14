"""
    pai.syntax
    ~~~~~~~~~~

    Module that defines the object representation of the language.
"""

__all__ = ['SyntaxError', 'Node', 'root', 'child']


GROUP_SIZE = 1
RTL = True
DELIMITER = ':'

ROOT_NODE_SIZE = 3
CHILD_NODE_SIZE = 2


ROOT_SENTINEL = object()


class SyntaxError(Exception):
    """
    Exception raised when then source string cannot be properly converted into an object representation.
    """


class Node:
    """
    Represents a single entity parsed from source.

    There are two types of nodes:
        "root": The first node parsed from source created from three values: "node", "edge", and "property".
        "child": Any additional nodes parsed after the root created from two values: "node" and "edge".

    There are three types of values:
        "node": Represents the entity/resource that is being described.
        "edge": Represents the relationship between the "node" and its "property" or its parent node if a child.
        "property": Represents a piece of information that will identify the "node".
    """

    __slots__ = ['node', 'edge', 'property', 'parent', 'child']

    def __init__(self, node, edge, property=None, parent=None, child=None):
        self.node = node
        self.edge = edge
        self.property = property
        self.parent = parent
        self.child = child

    def __repr__(self):
        return '<{}(node={}, edge={}, property={}>'.format(self.__class__.__name__, self.node,
                                                           self.edge, self.property)

    @property
    def is_root(self):
        """
        Flag to determine if this node is a "root" node.

        :return: `True` if a root node, `False` otherwise
        """
        return self.parent is ROOT_SENTINEL

    @property
    def is_child(self):
        """
        Flag to determine if this node is a "child" node.

        :return: `True` if a root node, `False` otherwise
        """
        return not self.is_root

    def link(self, parent):
        """
        Links this node as a "child" node of the given parent.

        :param parent: A :class:`~pai.syntax.Node` instance that will become the parent of this node
        :return: `None`
        """
        self.link_parent(parent)
        parent.link_child(self)

    def link_parent(self, parent):
        """
        Links the given node as the parent of this node.

        :param parent: A :class:`~pai.syntax.Node` instance that will become the parent of this node
        :return: `None`
        """
        if parent:
            self.parent = parent

    def link_child(self, child):
        """
        Links the given node as the child of this node.

        :param child: A :class:`~pai.syntax.Node` instance that will become the child of this node
        :return: `None`
        """
        if child:
            self.child = child


def root(node, edge, property):
    """
    Create a new "root" node with the given node, edge, and property.

    :param node: The entity/resource this root node represents
    :param edge: The relationship between this root node and its property
    :param property: The piece of information that describes the entity/resource
    :return: A :class:`~pai.syntax.Node` instance that is a root node
    """
    return Node(node, edge, property, ROOT_SENTINEL)


def child(node, edge, parent):
    """
    Create a new "child" node with the given node, edge, and parent node.

    :param node: The entity/resource this root node represents
    :param edge: The relationship between this root node and its parent
    :param parent: A :class:`~pai.syntax.Node` instance that is the parent of this child node
    :return: A :class:`~pai.syntax.Node` instance that is a child node
    """
    node = Node(node, edge)
    node.link(parent)
    return node
