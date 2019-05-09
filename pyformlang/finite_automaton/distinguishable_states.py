import array


class DistinguishableStates(object):

    def __init__(self, number_states):
        self.number_states = number_states + 1
        size_array = ((self.number_states + 1) ** 2)
        self.distinguishable = array.array('B', [False]) * size_array
        self.conversion = dict()
        self.conversion[None] = 0
        self.inverse_conversion = [None] * (self.number_states + 1)
        self.uniqueness_counter = 1

    def add(self, element):
        index = self._get_index(element)
        self.distinguishable[index] = True

    def _get_index(self, element):
        value0 = self._get_value(element[0])
        value1 = self._get_value(element[1])
        if value0 > value1:
            return value1 + self.number_states * value0
        return value0 + self.number_states * value1

    def _get_value(self, element):
        if element is None:
            return 0
        if element.index is not None:
            return element.index
        if element in self.conversion:
            value = self.conversion[element]
        else:
            self.conversion[element] = self.uniqueness_counter
            self.inverse_conversion[self.uniqueness_counter] = element
            self.uniqueness_counter += 1
            value = self.uniqueness_counter - 1
        element.index = value
        return value

    def __contains__(self, element):
        index = self._get_index(element)
        return self.distinguishable[index]

    def not_contains_and_add(self, element):
        index = self._get_index(element)
        contained = self.distinguishable[index]
        if not contained:
            self.distinguishable[index] = True
        return not contained

    def get_non_distinguishable(self):
        for i in range(1, self.number_states + 1):
            for j in range(i + 1, self.number_states + 1):
                index = i + self.number_states * j
                if not self.distinguishable[index]:
                    state0 = self.inverse_conversion[i]
                    state1 = self.inverse_conversion[j]
                    if state0 is not None and state1 is not None:
                        yield (state0, state1)
