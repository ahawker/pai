"""
    pai_lang.parser
    ~~~~~~~~~~~~~~~

    Module for parsing shell-safe strings based on the language as defined by :mod:`~pai.syntax`.
"""

from pai_lang import syntax, visitor
from pai_parser import parser


__all__ = ['parse', 'parse_gen']


def parse(data):
    """
    Create a list of nodes created by the visitor from the parsed data string.

    :param data: String to parse
    :return: List of nodes created by visitor
    """
    return list(parse_gen(data))


def parse_gen(data):
    """
    Generator function that yields nodes created by the visitor from the parsed data string.

    :param data: String to parse
    :return: List of nodes created by visitor
    """
    return parser.parse_gen(data, visitor, syntax.DELIMITER, syntax.GROUP_SIZE, syntax.RTL)
