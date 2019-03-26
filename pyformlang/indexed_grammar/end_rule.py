from .reduced_rule import ReducedRule


class EndRule(ReducedRule):
    """EndRule
    Represents an end rule, i.e. a rule of the form:
        A[sigma] -> a
    """

    def isEndRule(self):
        """isEndRule Indicates that it is an end rule"""
        return True

    def getLeftTerm(self):
        """getLeftTerm Gets the non-terminal on the left of the rule"""
        return self.leftTerm

    def getRightTerm(self):
        """getRightTerm Gets the terminal on the right of the rule"""
        return self.rightTerm

    def __init__(self, left, right):
        """__init__
        Initialises the end rule, i.e. a rule of the form:
            A[sigma] -> a
        :param left: The non-terminal on the left, "A" here
        :param right: The terminal on the right, "a" here
        """
        self.leftTerm = left
        self.rightTerm = right

    def getNonTerminals(self):
        """getTerminals Gets the non-terminals used"""
        return [self.leftTerm]

    def getTerminals(self):
        """getTerminals Gets the terminals used"""
        return {self.rightTerm}

    def __repr__(self):
        """__repr__ Gets the string representation of the rule"""
        return self.leftTerm + " -> " + self.rightTerm

    def __eq__(self, other):
        return other.isEndRule() and other.getLeftTerm() == self.getLeftTerm()\
            and other.getRightTerm() == self.getRightTerm()
