from bitarray import bitarray


class DistinguishableStates(object):

    def __init__(self, number_states):
        self.number_states = number_states + 1
        self.distinguishable = ((self.number_states + 1)  ** 2) * bitarray('0')
        self.conversion = dict()
        self.conversion[None] = 0
        self.uniqueness_counter = 1

    def add(self, element):
        index = self._get_index(element)
        self.distinguishable[index] = True
        index = self._get_index((element[1], element[0]))
        self.distinguishable[index] = True

    def _get_index(self, element):
        value0 = self._get_value(element[0])
        value1 = self._get_value(element[1])
        return value0 + self.number_states * value1

    def _get_value(self, element):
        if element in self.conversion:
            return self.conversion[element]
        else:
            self.conversion[element] = self.uniqueness_counter
            self.uniqueness_counter += 1
            return self.uniqueness_counter - 1

    def __contains__(self, element):
        index = self._get_index(element)
        return self.distinguishable[index]
