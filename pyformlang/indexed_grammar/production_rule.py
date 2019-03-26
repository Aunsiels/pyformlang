from .reduced_rule import ReducedRule


class ProductionRule(ReducedRule):
    """ProductionRule
    Represents a production rule, i.e. a rule of the form:
        A[sigma] -> B[r sigma]
    """

    def isProduction(self):
        """isProduction Indicates we have a production rule"""
        return True

    def getProduction(self):
        """getProduction Gets the terminal used in the production"""
        return self.production

    def getLeftTerm(self):
        """getLeftTerm Gets the non-terminal on the left side of the rule"""
        return self.leftTerm

    def getRightTerm(self):
        """getRightTerm Gets the non-terminal on the right side of the rule"""
        return self.rightTerm

    def __init__(self, left, right, prod):
        """__init__
        Initialises a production rule, i.e. a rule of the form:
            A[sigma] -> B[r sigma]
        :param left: The non-terminal on the left side of the rule, A here
        :param right: The non-terminal on the right side of the rule, B here
        :param prod: The terminal used in the rule, "r" here
        """
        self.production = prod
        self.leftTerm = left
        self.rightTerm = right

    def getNonTerminals(self):
        """getNonTerminals Gets the non-terminals used in the rule"""
        return [self.leftTerm, self.rightTerm]

    def getTerminals(self):
        """getTerminals Gets the terminals used in the rule"""
        return {}

    def __repr__(self):
        """__repr__ Gets the string representation of the rule"""
        return self.leftTerm + " -> " + \
            self.rightTerm + "[ " + self.production + " ]"

    def __eq__(self, other):
        return other.isProduction() and other.getLeftTerm() == \
            self.getLeftTerm() and other.getRightTerm() == self.getRightTerm()\
            and other.getProduction() == self.getProduction()
