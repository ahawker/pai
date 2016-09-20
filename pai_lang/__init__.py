"""
    pai_lang
    ~~~~~~~~

    Language for describing resources/relations as shell-safe strings.

    :copyright: (c) 2016 Andrew Hawker.
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import parser
from .parser import *
from . import syntax
from .syntax import *


__all__ = parser.__all__ + syntax.__all__


__version__ = '1.0.0'
