""" An abstract class to represent something which are be transformed into
a regex
"""

class Regexable(object):
    """ An abstract class to represent something which are be transformed into
    a regex
    """

    def to_regex(self) -> "Regex":
        """ Tranforms the EpsilonNFA to a regular expression

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            A regular expression equivalent to the current Epsilon NFA
        """
        raise NotImplementedError()

    def union(self, other: "Regexable") -> "EpsilonNFA":
        """ Makes the union of two regexable objects

        Parameters
        ----------
        other : :class:`~pyformlang.finite_automaton.Regexable`
            The other regexable object

        Returns
        ----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
        """
        regex0 = self.to_regex()
        regex1 = other.to_regex()
        regex = regex0.union(regex1)
        return regex.to_epsilon_nfa()
