#!/usr/bin/env python3 

import graphdata_4425
import rendering
import graphfuncs
import solvingfuncs
import sys
from PossiblePairs import PossiblePairs

# graph is organised with greater-than (gt) values -> less-than (lt) values

connections = dict(
    (chr(ord('A') + i), set()) for i in range(26)
)

# this is the  gt->lt connections, with indirect links pruned
direct_connections = dict()

# this is the  gt->lt connections, with indirect links fully elaborated
indirect_connections = dict()

# this is the  lt->gt connections, with indirect links pruned
direct_connections_inv = dict()

# this is the  lt->gt connections, with indirect links fully elaborated
indirect_connections_inv = dict()

possible_vals = set(i for i in range(26))

possibles = dict(
    (chr(ord('A') + i), possible_vals.copy()) for i in range(26)
)

possible_pairs = PossiblePairs.all_possibles()

for row in graphdata_4425.ACROSS:
    (number, l1, l2, l3, l4) = row
    graphfuncs.add_connection(connections, l1, l2)
    graphfuncs.add_connection(connections, l2, l3)
    graphfuncs.add_connection(connections, l3, l4)

for row in graphdata_4425.DOWN:
    (number, l1, l2, l3, l4) = row
    graphfuncs.add_connection(connections, l1, l2)
    graphfuncs.add_connection(connections, l2, l3)
    graphfuncs.add_connection(connections, l3, l4)

direct_connections = graphfuncs.prune_redundant_links(connections)
indirect_connections = graphfuncs.populate_indirect_links(direct_connections)
direct_connections_inv = graphfuncs.invert_graph(direct_connections)
indirect_connections_inv = graphfuncs.invert_graph(indirect_connections)


def dmin(l, default):
    try:
        return min(l)
    except:
        return default


def dmax(l, default):
    try:
        return max(l)
    except:
        return default


def diff_possibles(possibles_old, possibles_new):
    result = {}
    for key in sorted(possibles_old.keys()):
        diff = possibles_old[key] - possibles_new[key]
        if len(diff):
            result[key] = diff
    return result

# uncomment following line to add found extra solutions
# import exogenous_constraints;  exogenous_constraints.apply(possibles)

making_progress = True
while making_progress:
    print("main loop...", file=sys.stderr)
    making_progress = False

    print("apply_min_constraint..", file=sys.stderr)
    p = solvingfuncs.apply_min_constraint(indirect_connections, possibles)
    if p != possibles:
        print(diff_possibles(possibles, p), file=sys.stderr)
        possibles = p
        making_progress = True

    print("apply_max_constraint..", file=sys.stderr)
    p = solvingfuncs.apply_max_constraint(indirect_connections_inv, possibles)
    if p != possibles:
        print(diff_possibles(possibles, p), file=sys.stderr)
        possibles = p
        making_progress = True

    print("one_place_available_for_number..", file=sys.stderr)
    p = solvingfuncs.one_place_available_for_number(possibles)
    if p != possibles:
        print(diff_possibles(possibles, p), file=sys.stderr)
        possibles = p
        making_progress = True

    print("remove_solved_possibles..", file=sys.stderr)
    p = solvingfuncs.remove_solved_possibles(possibles)
    if p != possibles:
        print(diff_possibles(possibles, p), file=sys.stderr)
        possibles = p
        making_progress = True

    for clue in graphdata_4425.ACROSS:
        (p, pp) = solvingfuncs.reduce_with_clue2(possibles, possible_pairs, clue)
        print("ACROSS {}".format(clue), file=sys.stderr)
        if p != possibles or possible_pairs != pp:
            print(diff_possibles(possibles, p), file=sys.stderr)
            possibles = p
            possible_pairs = pp
            making_progress = True

    for clue in graphdata_4425.DOWN:
        print("DOWN   {}".format(clue), file=sys.stderr)
        (p, pp) = solvingfuncs.reduce_with_clue2(possibles, possible_pairs, clue)
        if p != possibles or possible_pairs != pp:
            print(diff_possibles(possibles, p), file=sys.stderr)
            possibles = p
            possible_pairs = pp
            making_progress = True


rendering.print_graph(direct_connections, possibles)
