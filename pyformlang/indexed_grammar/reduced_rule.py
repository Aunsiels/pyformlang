class ReducedRule(object):
    """ReducedRule
    Superobject of all possible reduced forms. They can be of
    four types :
        * Consumption
        * Production
        * End
        * Duplication
    """

    def isConsumption(self):
        """isConsumption Whether the rule is a consumption rule or not"""
        return False

    def isDuplication(self):
        """isDuplication Whether the rule is a duplication rule or not"""
        return False

    def isProduction(self):
        """isProduction Whether the rule is a production rule or not"""
        return False

    def isEndRule(self):
        """isEndRule Whether the rule is an end rule or not"""
        return False
