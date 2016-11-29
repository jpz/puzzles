from bitarray import bitarray

# using bitarray[num*num] as set( (num, num) ) as much too slow


class PossiblePairs(object):

    @classmethod
    def all_possibles(cls):
        """
        Return a new PossiblePairs instance, initialised with all possibilities being available,
        (A..Z, A..Z) = set (0..25)
        """
        me = cls()
        possible_pair_vals = bitarray("1"*26*26)
        me.possible_pairs = dict(
            ((chr(ord('A') + i), chr(ord('A') + j)), possible_pair_vals.copy())
            for i in range(26) for j in range(26) if i != j
        )
        return me

    @classmethod
    def blank_possibles(cls, letters):
        """
        Return a new PossiblePairs instance, initialised with no possibilities being available, for each
        letter combination.
        """
        me = cls()
        me.possible_pairs = {}
        possible_pair_vals = bitarray("0"*26*26)

        letters = list(set(letters))
        for idx, first in enumerate(letters):
            for second in letters[idx + 1:]:
                me.possible_pairs[first, second] = possible_pair_vals.copy()
                me.possible_pairs[second, first] = possible_pair_vals.copy()
        return me

    def __init__(self):
        """
        Not intended to be called directly
        """
        self.possible_pairs = {}

    def __eq__(self, other):
        """We need to test PossiblePairs for equality"""
        return self.possible_pairs == other.possible_pairs

    def are_possible_pairs(self, key_val):
        """
        :param key_val: A dictionary of letter -> number
        :return: True iff all combinations of letters in the dictionary and corresponding values appears in possible_pairs
        """
        letters = list(key_val.keys())
        for idx, first in enumerate(letters):
            for second in letters[idx + 1:]:
                if not self.possible_pairs[(first, second)][self._index(key_val[first], key_val[second])]:
                    return False
        return True

    def add_possible_pairs(self, key_value):
        """
        :param key_value: a dictionary of letter -> number
        :return: None
        """
        letters = list(key_value.keys())
        for idx, first in enumerate(letters):
            for second in letters[idx + 1:]:
                self.possible_pairs[(first, second)][self._index(key_value[first], key_value[second])] = True
                self.possible_pairs[(second, first)][self._index(key_value[second], key_value[first])] = True

    def intersect_update(self, new_pairs):
        """
        restrict the possible pairs with the sets of contained in new_pairs (which is also a PossiblePairs instance)
        :param new_pairs:
        :return: True if pairs were updated
        """
        updated = False
        for k, v in new_pairs.possible_pairs.items():
            intersect = self.possible_pairs[k] & v
            if intersect != self.possible_pairs[k]:
                updated = True
                self.possible_pairs[k] = intersect
        return updated

    def _index(self, a, b):
        """
        Returns the index into a bit array for (number, number)
        :param a:
        :param b:
        :return: a*26 + b
        """
        return a*26 + b

