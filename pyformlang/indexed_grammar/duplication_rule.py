from .reduced_rule import ReducedRule


class DuplicationRule(ReducedRule):
    """DuplicationRule
    Represents a duplication rule, i.e. a rule of the form:
        A[sigma] -> B[sigma] C[sigma]
    """

    def isDuplication(self):
        """isDuplication Proves it is a duplication rule"""
        return True

    def getRightTerms(self):
        """getRightTerms Gives the non-terminals on the right of the rule
        as a tuple"""
        return self.rightTerms

    def getLeftTerm(self):
        """getLeftTerm Gives the non-terminal on the left of the rule"""
        return self.leftTerm

    def __init__(self, leftTerm, rightTerm0, rightTerm1):
        """__init__
        Initialises the duplication rule of the form:
            A[sigma] -> B[sigma] C[sigma]
        :param leftTerm: The non-terminal on the left of the rule (A here)
        :param rightTerm0: The first non-terminal on the right of the rule
        (B here)
        :param rightTerm1: The second non-terminal on the right of the rule
        (C here)
        """
        self.leftTerm = leftTerm
        self.rightTerms = (rightTerm0, rightTerm1)

    def getNonTerminals(self):
        """getNonTerminals Gives the set of non-terminals used in this rule"""
        return [self.leftTerm, self.rightTerms[0], self.rightTerms[1]]

    def getTerminals(self):
        """getTerminals Gets the terminals used in the rule"""
        return {}

    def __repr__(self):
        """__repr__ Gives a string representation of the rule, ignoring the
        sigmas"""
        return self.leftTerm + " -> " + self.rightTerms[0] + \
            " " + self.rightTerms[1]

    def __eq__(self, other):
        return other.isDuplication() and other.getLeftTerm() == \
            self.getLeftTerm() and other.getRightTerms() == self.getRightTerms()
