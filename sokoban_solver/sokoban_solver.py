#!/usr/bin/env python

# sokoban solver, Jason Zavaglia 14/1/2015


#  representation of board:
#
#  # - wall
#  X - target square
#  B - box
#  . - blank space
#  * - person
#
# Note that two boards are encoded, contains
# location of X's, and the other contains
# location of boxes.
#
# Note any line starting with # is a map,
# any other line is ignored.  Two maps are expected,
# and walls must agree.
#
#  e.g.
#
# #######
# ## X ##
# ## X ##
# ## X ##
# #  X ##
# #  X  #
# #  X  #
# ###  ##
# #######
#
# #######
# ## * ##
# ##B B##
# ## B ##
# #  B ##
# #  B  #
# #  B  #
# ###  ##
# #######


class BoardState(object):

    __slots__ = ['board', 'target_locations', 'person_location', 'box_locations']

    def __init__(self, board, target_locations, person_location, box_locations):

        # ensuring members are tuples and frozensets ensures
        # the object is hashable, and can be put in a dictionary and set
        if type(board).__name__ <> 'tuple':
            board = tuple(board)
        if type(target_locations).__name__ <> 'frozenset':
            target_locations = frozenset(target_locations)
        if type(person_location).__name__ <> 'tuple':
            person_location = tuple(person_location)
        if type(box_locations).__name__ <> 'frozenset':
            box_locations = frozenset(box_locations)

        self.board = board
        self.target_locations = target_locations
        self.person_location = person_location
        self.box_locations = box_locations

    def __hash__(self):
        return hash((self.board, self.person_location, self.box_locations))

    def __eq__(self, other):
        return (self.board, self.person_location, self.box_locations) == (other.board, other.person_location, other.box_locations)

    def calculate_move_to_cell(self, location, direction):
        """ Helper function to calculate move-to cell """
        tr, tc = location
        if direction == 'U':
            tr = tr - 1
        elif direction == 'D':
            tr = tr + 1
        elif direction == 'L':
            tc = tc - 1
        elif direction == 'R':
            tc = tc + 1
        else:
            raise Exception("bad direction: '{}'".format(direction))
        return (tr, tc)

    def is_within_bounds(self, location):
        """ Helper function to determine if a move-to cell is within bounds """
        r, c = location
        if r < 0 or c < 0 or r > len(self.board)-1 or c > len(self.board[0])-1:
            return False
        else:
            return True

    def can_move(self, direction):
        """ can the person move in this direction? """
        tr, tc = self.calculate_move_to_cell(self.person_location, direction)

        if not self.is_within_bounds((tr, tc)):
            return False

        if self.board[tr][tc] == '#':
            return False
        elif (tr, tc) in self.box_locations:
            return self.box_can_move((tr,tc), direction)
        else:
            return True

    def box_can_move(self, box_location, direction):
        """ can a box be pushed in this direction? """
        tr, tc = self.calculate_move_to_cell(box_location, direction)

        if not self.is_within_bounds((tr, tc)):
            return False

        if self.board[tr][tc] == '#':
            return False
        elif (tr, tc) in self.box_locations:
            return False
        else:
            return True

    def is_solved(self):
        return self.box_locations == self.target_locations

    def move(self, direction):
        tr, tc = self.calculate_move_to_cell(self.person_location, direction)
        box_locations = set(self.box_locations)
        if (tr, tc) in box_locations:
            br, bc = self.calculate_move_to_cell((tr, tc), direction)
            box_locations.remove((tr, tc))
            box_locations.add((br, bc))
        return BoardState(self.board, self.target_locations, (tr, tc), box_locations)


def read_board(stream):
    have_read_board1 = False
    have_read_board2 = False
    board1 = []
    board2 = []

    for line in stream:
        if len(line) > 0 and line[0] == '#':
            if not have_read_board1:
                board1.append(line.rstrip())
            elif not have_read_board2:
                board2.append(line.rstrip())
            else:
                raise Exception("bad format: third '#'-commencing block found")
        else:
            if len(board1):
                have_read_board1 = True
            if len(board2):
                have_read_board2 = True

    if len(board1) == 0:
        raise Exception("no boards present")

    if len(board2) == 0:
        raise Exception("second board not present")

    if len(board1) <> len(board2):
        raise Exception("board pair have different row count")

    row_count = len(board1)
    column_count = len(board1[0])

    for row in board1:
        if column_count <> len(row):
            raise Exception("column counts are inconsistent")

    for row in board2:
        if column_count <> len(row):
            raise Exception("column counts are inconsistent")

    for r in xrange(row_count):
        for c in xrange(column_count):
            if board1[r][c] == '#' and board2[r][c] <> '#':
                raise Exception("walls are inconsistent")
            if board1[r][c] not in ('#', ' ', 'X'):
                raise Exception("unexpected character '{}' found in first board".format(board[r][c]))
            if board2[r][c] not in ('#', ' ', '*', 'B'):
                raise Exception("unexpected character '{}' found in second board".format(board[r][c]))

    person_location = None
    target_locations = set()
    box_locations = set()

    for r in xrange(row_count):
        for c in xrange(column_count):
            if board1[r][c] == 'X':
                target_locations.add((r, c))
            if board2[r][c] == '*':
                person_location = (r, c)
            if board2[r][c] == 'B':
                box_locations.add( (r, c) )

    state = BoardState(board1, target_locations, person_location, box_locations)

    return state


def main():
    import sys, collections

    if len(sys.argv) != 2:
        print "usage: sokoban_solver.py mapfile"
        exit(1)

    f = open(sys.argv[1])

    state = read_board(f)

    # simple breadth-first search of board states

    move_to_get_to = {}
    parent = {}
    queue = collections.deque()
    move_to_get_to[state] = ''
    parent[state] = None
    queue.append(state)
    solution = None

    cnt = 0
    while(len(queue)):
        s = queue.popleft()
        if s.is_solved():
            solution = s
            break
        for direction in ('U', 'D', 'L', 'R'):
            if s.can_move(direction):
                new_s = s.move(direction)
                if new_s not in move_to_get_to:
                    move_to_get_to[new_s] = direction
                    parent[new_s] = s
                    queue.append(new_s)

    moves = []
    while solution:
        # if stops us adding the very first entry where direction == ''
        if move_to_get_to[solution]:
            moves.append(move_to_get_to[solution])
        solution = parent[solution]
    moves.reverse()

    if len(moves) == 0:
        print "no solution found"
    else:
        print "solution: "
        for i, elem in enumerate(moves):
            print i+1, elem


if __name__ == "__main__":
    main()
