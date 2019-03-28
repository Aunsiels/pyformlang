"""
Representation of a reduced rule
"""


class ReducedRule(object):
    """Representation of all possible reduced forms.
    They can be of four types :
        * Consumption
        * Production
        * End
        * Duplication
    """

    def is_consumption(self) -> bool:
        """Whether the rule is a consumption rule or not

        Returns
        ----------
        is_consumption : bool
            Whether the rule is a consumption rule or not
        """
        return False

    def is_duplication(self) -> bool:
        """Whether the rule is a duplication rule or not

        Returns
        ----------
        is_duplication : bool
            Whether the rule is a duplication rule or not
        """
        return False

    def is_production(self) -> bool:
        """Whether the rule is a production rule or not

        Returns
        ----------
        is_production : bool
            Whether the rule is a production rule or not
        """
        return False

    def is_end_rule(self) -> bool:
        """Whether the rule is an end rule or not

        Returns
        ----------
        is_end : bool
            Whether the rule is an end rule or not
        """
        return False
