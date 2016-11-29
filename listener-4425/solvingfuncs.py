from copy import deepcopy
import foursquares
import graphdata_4425
from PossiblePairs import PossiblePairs


# Some solving functions for this specific puzzle, the algorithms below reduce / exhaust the possible
# values for each cell, with invariants that 1) parent nodes are greater than child nodes, 2) all nodes have
# a unique value in the range of [0..25], 3) all clues are length > 1, and 4) all clues are the highest precedent
# sum of squares solution for any given number (in accordance with rules as stated in other places)

def apply_max_constraint(linked_nodes_bigger, possibles):
    """
    Use the maximas of higher numbered, direct or indirect parent nodes to calculate maxima of this node.
    The list of maximas is reverse ordered, and the count of nodes is used to reduce the maxima.
    e.g. for 25, 25, 25, 24, the first element implies that the maxima will be 21 or less.  For
    each element this calculation is done, for instance 25, 8, 8, 8 would rely on the calculation
    of the 2nd node, which would be 8 - 3 = 5 maxima.
    """
    possibles = deepcopy(possibles)
    making_progress = True
    while making_progress:
        making_progress = False
        for a in sorted(linked_nodes_bigger):
            # get the smallest max value for all parents (min/max)
            if len(linked_nodes_bigger[a]) == 0:
                continue
            max_constraint = 999
            maxs = sorted([max(possibles[b]) for b in linked_nodes_bigger[a]], reverse=True)
            for (i, m) in enumerate(maxs):
                max_constraint = min(m - (len(maxs) - i), max_constraint)
            if max(possibles[a]) > max_constraint:
                making_progress = True
                possibles[a].difference_update([n for n in range(max_constraint + 1, 50)])
    return possibles


def apply_min_constraint(linked_nodes_smaller, possibles):
    """
    Inverse of the apply_max_constraints:
    Use the minimas of directly or indirectly linked child nodes to calculate minima of this node.
    The list of minimas is regularly ordered, and the count of nodes is used to increase the minima.
    e.g. for 0, 0, 0, 1, the first element implies that the mimima will be 4 or more.  For
    each element this calculation is done, for instance 0, 3, 3, 3 would rely on the calculation
    of the 2nd node, which would be 3 + 3 = 6 maxima.
    """
    possibles = deepcopy(possibles)
    making_progress = True
    while making_progress:
        making_progress = False
        for a in sorted(linked_nodes_smaller):
            # get the smallest max value for all parents (min/max)
            if len(linked_nodes_smaller[a]) == 0:
                continue
            min_constraint = -1
            mins = sorted([min(possibles[b]) for b in linked_nodes_smaller[a]])
            for (i, m) in enumerate(mins):
                min_constraint = max(m + (len(mins) - i), min_constraint)
            if min(possibles[a]) < min_constraint:
                making_progress = True
                possibles[a].difference_update([n for n in range(min_constraint)])
    return possibles


def reduce_with_clue(possibles, clue):
    """
    Using the possible values for each of the cells, find all values for each of the letters where
    it holds true that the 4 letters make up the highest ranked four-square number.  As per the puzzle,
    for X = A^2 + B^2 + C^2 + D^2, there must be no combination of smaller list of squares which equals X,
    and there must be no answer of the same number of squares, which has higher numbers.

    This function therefore calculates all values of X for all possible values of letters l1, l2, l3, l4,
    and regards those given values of l1, l2, l3, l4 where those values are the highest precedence four-square
    as valid candidates for those letters.

    :param possibles: a map of letter -> set(numbers)
    :param clue: a 5-tuple of (_, letter, letter, letter, letter)
    :return: copy of possibles with reduced set of values
    """
    possibles = deepcopy(possibles)
    (_, l1, l2, l3, l4) = clue
    good1s = set()
    good2s = set()
    good3s = set()
    good4s = set()
    for n4 in possibles[l4]:
        if l3 == l4:
            l3it = [n4]
        else:
            # required that n3 < n4
            l3it = possibles[l3] - set(range(n4 + 1))
        for n3 in l3it:
            if l2 == l3:
                l2it = [n3]
            else:
                # required that n2 < n3
                l2it = possibles[l2] - set(range(n3 + 1))
            for n2 in l2it:
                if l1 == l2:
                    l1it = [n2]
                else:
                    # required that n1 < n2
                    l1it = possibles[l1] - set(range(n2 + 1))
                for n1 in l1it:
                    # added an extra constraint that a solution must be longer than a single digit
                    if foursquares.is_foursquare([n1, n2, n3, n4]) and foursquares.sum_of_squares([n1, n2, n3, n4]) > 9:
                        good1s.add(n1)
                        good2s.add(n2)
                        good3s.add(n3)
                        good4s.add(n4)
    possibles[l1] = good1s
    possibles[l2] = good2s
    possibles[l3] = good3s
    possibles[l4] = good4s
    return possibles


def reduce_with_clue2(possibles, possible_pairs, clue):
    """
    Using the possible values for each of the cells, find all values for each of the letters where
    it holds true that the 4 letters make up the highest ranked four-square number.  As per the puzzle,
    for X = A^2 + B^2 + C^2 + D^2, there must be no combination of smaller list of squares which equals X,
    and there must be no answer of the same number of squares, which has higher numbers.

    This function therefore calculates all values of X for all possible values of letters l1, l2, l3, l4,
    and regards those given values of l1, l2, l3, l4 where those values are the highest precedence four-square
    as valid candidates for those letters.

    Note that this function has been adapted from reduce_with_clue() to include reduction of paired correlated values,
    thus is A = 2 and B = 1 is seen as well as A = 4 and B = 2, then (A,B) can be either (4,2), or (2,1)

    This improves the exhaustion of possibles for given letters.

    :param possibles: a map of letter -> set(numbers)
    :param possible_pairs: a map of letter -> set(numbers)
    :param clue: a 5-tuple of (_, letter, letter, letter, letter)
    :return: (copy of possibles with reduced set of values, copy of possible_pairs with reduced set of values)
    """
    possibles = deepcopy(possibles)
    possible_pairs = deepcopy(possible_pairs)
    (_, l1, l2, l3, l4) = clue
    good1s = set()
    good2s = set()
    good3s = set()
    good4s = set()
    new_pairs = PossiblePairs.blank_possibles([l1, l2, l3, l4])
    for n4 in possibles[l4]:
        if l3 == l4:
            l3it = [n4]
        else:
            # required that n3 < n4
            l3it = possibles[l3] - set(range(n4 + 1))
        for n3 in l3it:
            if l2 == l3:
                l2it = [n3]
            else:
                # required that n2 < n3
                l2it = possibles[l2] - set(range(n3 + 1))
            for n2 in l2it:
                if l1 == l2:
                    l1it = [n2]
                else:
                    # required that n1 < n2
                    l1it = possibles[l1] - set(range(n2 + 1))
                for n1 in l1it:
                    # added an extra constraint that a solution must be longer than a single digit
                    if (foursquares.is_foursquare([n1, n2, n3, n4]) and
                            foursquares.sum_of_squares([n1, n2, n3, n4]) > 9 and
                            possible_pairs.are_possible_pairs({l1: n1, l2: n2, l3: n3, l4: n4})):
                        good1s.add(n1)
                        good2s.add(n2)
                        good3s.add(n3)
                        good4s.add(n4)
                        new_pairs.add_possible_pairs({l1: n1, l2: n2, l3: n3, l4: n4})

    possibles[l1].intersection_update(good1s)
    possibles[l2].intersection_update(good2s)
    possibles[l3].intersection_update(good3s)
    possibles[l4].intersection_update(good4s)
    possible_pairs.intersect_update(new_pairs)
    return possibles, possible_pairs


def one_place_available_for_number(possibles):
    """If there is only one place where a number can appear, we search for those occurrences"""
    possibles = deepcopy(possibles)
    for n in graphdata_4425.NUMBERS:
        count = 0
        for it in possibles:
            if n in possibles[it]:
                found_at = it
                count += 1
        if count == 1:
            possibles[found_at] = {n}
    return possibles


def remove_solved_possibles(possibles):
    """If a possible is solved, ensure it does not appear as a possible elsewhere"""
    new_possibles = deepcopy(possibles)
    for it in possibles:
        if len(possibles[it]) == 1:
            for n in possibles:
                if n != it:
                    new_possibles[n].difference_update(possibles[it])
    return new_possibles
