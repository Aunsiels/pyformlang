"""
Representation of a reduced rule
"""


class ReducedRule:
    """Representation of all possible reduced forms.
    They can be of four types :
        * Consumption
        * Production
        * End
        * Duplication
    """

    @staticmethod
    def is_consumption() -> bool:
        """Whether the rule is a consumption rule or not

        Returns
        ----------
        is_consumption : bool
            Whether the rule is a consumption rule or not
        """
        return False

    @staticmethod
    def is_duplication() -> bool:
        """Whether the rule is a duplication rule or not

        Returns
        ----------
        is_duplication : bool
            Whether the rule is a duplication rule or not
        """
        return False

    @staticmethod
    def is_production() -> bool:
        """Whether the rule is a production rule or not

        Returns
        ----------
        is_production : bool
            Whether the rule is a production rule or not
        """
        return False

    @staticmethod
    def is_end_rule() -> bool:
        """Whether the rule is an end rule or not

        Returns
        ----------
        is_end : bool
            Whether the rule is an end rule or not
        """
        return False

    @property
    def f_parameter(self):
        """The f parameter

        Returns
        ----------
        f : any
            The f parameter
        """
        raise NotImplementedError

    @property
    def left_term(self):
        """The left term

        Returns
        ----------
        left_term : any
            The left term of the rule
        """
        raise NotImplementedError

    @property
    def right_terms(self):
        """The right terms

        Returns
        ----------
        right_terms : iterable of any
            The right terms of the rule
        """
        raise NotImplementedError

    @property
    def right_term(self):
        """The unique right term

        Returns
        ----------
        right_term : iterable of any
            The unique right term of the rule
        """
        raise NotImplementedError

    @property
    def production(self):
        """The production

        Returns
        ----------
        right_terms : any
            The production
        """
        raise NotImplementedError
