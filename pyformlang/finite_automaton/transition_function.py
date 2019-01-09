class TransitionFunction(object):
    """ A transition function in a finite automaton.

    This is a deterministic transition function.

    Parameters
    ----------

    Attributes
    ----------
    _transitions : dict
        A dictionary which contains the transitions of a finite automaton


    """

    def __init__(self):
        self._transitions = dict()

    def add_transition(self, s_from, by, s_to):
        """ Adds a new transition to the function

        Parameters
        ----------
        s_from : State
            The source state
        by : Symbol
            The transition symbol
        s_to : State
            The destination state


        Returns
        --------
        done : int
            Always 1

        Raises
        --------
        DuplicateTransitionError
            If the transition already exists
        """
        if s_from in self._transitions:
            if by in self._transitions[s_from]:
                if self._transitions[s_from][by] != s_to:
                    raise DuplicateTransitionError(s_from,
                                                   by,
                                                   s_to,
                                                   self._transitions[s_from][by])
            else:
                self._transitions[s_from][by] = s_to
        else:
            self._transitions[s_from] = dict()
            self._transitions[s_from][by] = s_to
        return 1



class DuplicateTransitionError(Exception):
    """ Signals a duplicated transition

    Parameters
    ----------
    s_from : :class:`~pyformlang.finite_automaton.State`
        The source state
    by : :class:`~pyformlang.finite_automaton.Symbol`
        The transition symbol
    s_to : :class:`~pyformlang.finite_automaton.State`
        The wanted new destination state
    s_to_old : :class:`~pyformlang.finite_automaton.State`
        The old destination state

    Attributes
    ----------
    message : str
        An error message summarising the information

    """

    def __init__(self, s_from, by, s_to, s_to_old):
        self.message = "Transition from " + str(s_from) + " by " + str(by) +\
            " goes to " + str(s_to_old) + " not " + str(s_to)
        self._s_from = s_from
        self._by = by
        self._s_to = s_to
        self._s_to_old = s_to_old
