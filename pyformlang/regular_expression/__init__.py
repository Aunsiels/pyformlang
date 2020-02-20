"""
:mod:`pyformlang.regular_expression`
====================================

This module deals with regular expression.

By default, this module does not use the standard way to write regular
expressions. Please read the documentation of Regex for more information.

Available Classes
-----------------

Regex
    A regular expression
MisformedRegexError
    An error occurring when the input regex is incorrect

"""


from .regex import Regex
from .regex_objects import MisformedRegexError

__all__ = ["Regex", "MisformedRegexError"]