"""
Representation of a recursive automaton
"""

from typing import Dict, Set, AbstractSet, Optional, Hashable, Any

from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton.utils import to_symbol
from pyformlang.regular_expression import Regex
from pyformlang.cfg import Epsilon

from .box import Box


class RecursiveAutomaton:
    """ Represents a recursive automaton

    This class represents a recursive automaton.

    Parameters
    ----------
    start_box : :class:`~pyformlang.rsa.Box`
        Start box
    boxes : set of :class:`~pyformlang.rsa.Box`
        A finite set of boxes

    """

    def __init__(self,
                 start_box: Box,
                 boxes: AbstractSet[Box]) -> None:
        self._nonterminal_to_box: Dict[Symbol, Box] = {}
        self._start_nonterminal = start_box.nonterminal
        if start_box not in boxes:
            self._nonterminal_to_box[start_box.nonterminal] = start_box
        for box in boxes:
            self._nonterminal_to_box[box.nonterminal] = box

    @property
    def nonterminals(self) -> Set[Symbol]:
        """ The set of nonterminals """
        return set(self._nonterminal_to_box.keys())

    @property
    def boxes(self) -> Set[Box]:
        """ The set of boxes """
        return set(self._nonterminal_to_box.values())

    @property
    def start_nonterminal(self) -> Symbol:
        """ The start nonterminal """
        return self._start_nonterminal

    @property
    def start_box(self) -> Box:
        """ The start box """
        return self._nonterminal_to_box[self.start_nonterminal]

    def get_box_by_nonterminal(self, nonterminal: Hashable) -> Optional[Box]:
        """
        Box by nonterminal

        Parameters
        ----------
        nonterminal: :class:`~pyformlang.finite_automaton.Symbol` | str
            the nonterminal of which represents a box

        Returns
        -----------
        box : :class:`~pyformlang.rsa.Box` | None
            box represented by given nonterminal
        """

        nonterminal = to_symbol(nonterminal)
        return self._nonterminal_to_box.get(nonterminal, None)

    def get_number_boxes(self) -> int:
        """ Size of set of boxes """
        return len(self._nonterminal_to_box)

    @classmethod
    def from_regex(cls, regex: Regex, start_nonterminal: Hashable) \
            -> "RecursiveAutomaton":
        """ Create a recursive automaton from regular expression

        Parameters
        -----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The regular expression
        start_nonterminal : :class:`~pyformlang.finite_automaton.Symbol` | str
            The start nonterminal for the recursive automaton

        Returns
        -----------
        rsa : :class:`~pyformlang.rsa.RecursiveAutomaton`
            The new recursive automaton built from regular expression
        """
        start_nonterminal = to_symbol(start_nonterminal)
        box = Box(regex.to_minimal_dfa(), start_nonterminal)
        return RecursiveAutomaton(box, {box})

    @classmethod
    def from_ebnf(cls, text: str, start_nonterminal: Hashable = Symbol("S")) \
            -> "RecursiveAutomaton":
        """ Create a recursive automaton from ebnf \
            (ebnf = Extended Backus-Naur Form)

        Parameters
        -----------
        text : str
            The text of transform
        start_nonterminal : \
            :class:`~pyformlang.finite_automaton.Symbol` | str, optional
            The start nonterminal, S by default

        Returns
        -----------
        rsa : :class:`~pyformlang.rsa.RecursiveAutomaton`
            The new recursive automaton built from context-free grammar
        """
        start_nonterminal = to_symbol(start_nonterminal)
        productions: Dict[Hashable, str] = {}
        boxes = set()
        nonterminals = set()
        for production in text.splitlines():
            production = production.strip()
            if "->" not in production:
                continue

            head, body = production.split("->")
            head = head.strip()
            body = body.strip()
            nonterminals.add(to_symbol(head))

            if body == "":
                body = Epsilon().to_text()

            if head in productions:
                productions[head] += " | " + body
            else:
                productions[head] = body

        for head, body in productions.items():
            boxes.add(Box(Regex(body).to_minimal_dfa(), to_symbol(head)))
        start_box_dfa = Regex(productions[start_nonterminal.value]) \
            .to_minimal_dfa()
        start_box = Box(start_box_dfa, start_nonterminal)
        return RecursiveAutomaton(start_box, boxes)

    def is_equal_to(self, other: "RecursiveAutomaton") -> bool:
        """
        Check whether two recursive automata are equals by boxes.
        Not equivalency in terms of formal languages theory, just mapping boxes

        Parameters
        ----------
        other : :class:`~pyformlang.rsa.RecursiveAutomaton`
            The input recursive automaton

        Returns
        ----------
        are_equivalent : bool
            Whether the two recursive automata are equals or not
        """
        return self.boxes == other.boxes

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RecursiveAutomaton):
            return False
        return self.is_equal_to(other)

    def to_dot(self) -> str:
        """ Create dot representation of recursive automaton """
        dot_string = 'digraph "" {'
        for box in self._nonterminal_to_box.values():
            dot_string += f'\n{box.to_subgraph_dot()}'
        dot_string += "\n}"
        return dot_string
