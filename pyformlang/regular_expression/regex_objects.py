class Node(object): # pylint: disable=too-few-public-methods
    """ Represents a node in the tree representation of a regex

    Parameters
    ----------
    value : str
        The value of the node
    """

    def __init__(self, value):
        self._value = value

    def get_value(self):
        """ Give the value of the node

        Returns
        ----------
        value : str
            The value of the node
        """
        return self._value


CONCATENATION_SYMBOLS = ["."]
UNION_SYMBOLS = ["|", "+"]
KLEENE_STAR_SYMBOLS = ["*"]
EPSILON_SYMBOLS = ["epsilon", "$"]


def to_node(value: str) -> Node:
    """ Transforms a given value into a node """
    if not value:
        return Empty()
    if value in CONCATENATION_SYMBOLS:
        return Concatenation()
    if value in UNION_SYMBOLS:
        return Union()
    if value in KLEENE_STAR_SYMBOLS:
        return KleeneStar()
    if value in EPSILON_SYMBOLS:
        return Epsilon()
    return Symbol(value)


class Operator(Node): # pylint: disable=too-few-public-methods
    """ Represents an operator

    Parameters
    ----------
    value : str
        The value of the operator
    """

    def __repr__(self):
        return "Operator(" + str(self._value) + ")"


class Symbol(Node): # pylint: disable=too-few-public-methods
    """ Represents a symbol

    Parameters
    ----------
    value : str
        The value of the symbol
    """

    def __repr__(self):
        return "Symbol(" + str(self._value) + ")"


class Concatenation(Operator): # pylint: disable=too-few-public-methods
    """ Represents a concatenation
    """

    def __init__(self):
        super().__init__("Concatenation")


class Union(Operator): # pylint: disable=too-few-public-methods
    """ Represents a union
    """

    def __init__(self):
        super().__init__("Union")


class KleeneStar(Operator): # pylint: disable=too-few-public-methods
    """ Represents an epsilon symbol
    """

    def __init__(self):
        super().__init__("Kleene Star")


class Epsilon(Symbol): # pylint: disable=too-few-public-methods
    """ Represents an epsilon symbol
    """

    def __init__(self):
        super().__init__("Epsilon")


class Empty(Symbol): # pylint: disable=too-few-public-methods
    """ Represents an empty symbol
    """

    def __init__(self):
        super().__init__("Empty")


class MisformedRegexError(Exception):
    """ Error for misformed regex """

    def __init__(self, message: str, regex: str):
        super().__init__(message + " Regex: " + regex)
        self._regex = regex