from .reduced_rule import ReducedRule


class ConsumptionRule(ReducedRule):
    """ConsumptionRule
        Contains a representation of a consumption rule, i.e. a rule of the
        form:
            C[ r sigma] -> B[sigma]
    """

    def isConsumption(self):
        """isConsumption Indicates we have a consumption function"""
        return True

    def getF(self):
        """getF Gets the symbole which is consumed"""
        return self.f

    def getRight(self):
        """getRight Gets the symbole on the right of the rule"""
        return self.right

    def getLeftTerm(self):
        """getLeftTerm Gets the symbole on the left of the rule"""
        return self.left

    def __init__(self, f, left, right):
        """__init_ Initialises a rule of the form:
            C[ f sigma] -> B[sigma]
        :param f: The consummed symbole
        :param left: The non terminal on the left (here C)
        :param right: The non terminal on the right (here B)
        """
        self.f = f
        self.right = right
        self.left = left

    def getNonTerminals(self):
        """getNonTerminals Gets the non-terminals used in the rule"""
        return [self.left, self.right]

    def getTerminals(self):
        """getTerminals Gets the terminals used in the rule"""
        return {self.f}

    def __repr__(self):
        """__repr__ Gives the string representation of the rule, ignoring the
        sigmas"""
        return self.left + " [ " + self.f + " ] -> " + self.right

    def __eq__(self, other):
        return other.isConsumption() and other.getLeftTerm() == \
            self.getLeftTerm() and other.getRight() == self.getRight() and\
            other.getF() == self.getF()
