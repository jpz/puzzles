#
#  The following are incrementally hand-entered solutions, working with entry of solutions into grid.
#


def apply(possibles):
    #
    # G=4 deduced
    #
    # 37ac = GGGD (48 768) and 32dn = GXXD (24,264)
    # only intersection that makes sense if is 37ac = 48
    # therefore G = 4

    possibles['G'] = {4}

    # R = 10/20 deduced
    #
    # 8ac must start line 2, as "8ac" is too highly numbered for top row.
    # as the 2nd cell of row 2 is a 0, it therefore is deducible that 8ac starts
    # in the first cell of row 2.
    #
    # The only answers for R where the second digit is 0 are R = 10 or 20
    #

    possibles['R'] = {10, 20}

    # Further reductions sees that R = 10 is only solution
    # as 8dn = 17 and first digit = 1, therefore 8ac = 102

    possibles['R'] = {10}

    # 3dn second digit thus is 2, 3dn can only be 72 with J = 6

    possibles['J'] = {6}

    # 3ac therefore starts with 7, and thus N can only be 19

    possibles['N'] = {19}

    # 36ac must end with 6, therefore Q = 24 and 26ac = 616

    possibles['Q'] = {24}

    # 9ac is length 3 and starts in cell 4, therefore 11ac PXXD is length 2
    # this restricts P to being 5 or 7, and 9ac to 33 or 57

    possibles['P'] = {5, 7}

    # 4dn starts with 4, this restricts C = 14 as it is the only available solution
    # where CPDD first digit is 2 (from 221)

    possibles['C'] = {14}

    # 11ac starts with 3, as 6dn is 236 - only answer is 33 where P = 5

    possibles['P'] = {5}

    # 5ac and 5dn both involve Z.  After intersections with 9ac and 6dn, we deduce Z is restricted to 15 & 25

    possibles['Z'] = {15,25}

    # 7dn allows us to solve for K = 8

    possibles['K'] = {8}

    # 13dn - ECDD starts with 6, only solutions are E in 21, 22

    possibles['E'] = {21,22}

    # 14ac - MPTD has middle number 1, only solution is M = 22

    possibles['M'] = {22}

    # 10dn - only solution starting with digits 10 is U = 20

    possibles['U'] = {20}

    # 14dn - SBDD starts with 5 - only matching solutions where
    # B  = 3 and S = 7 or 23

    possibles['B'] = {3}
    possibles['S'] = {7, 23}

    # 35ac - LBDD is 3 digits and starts with 1 - L is restricted to {11, 13}

    possibles['L'] = {11, 13}

    # 26dn - FFDD is 3 digits and matches ?40 or ?48 - only solution is F = 18

    possibles['F'] = {18}

    # 35ac - LBDD must now match last digit = 8 therefore L = 13

    possibles['L'] = {13}

    # 25dn - YBBD must end in 07 - Y = 17 is only answer

    possibles['Y'] = {17}

    # 14dn - SBDD starts with 53, S = 23 is only answer

    possibles['S'] = {23}

    # 18ac - OJDD starts with 11, only solution O = 9

    possibles['O'] = {9}

    # 21ac - HXXD = 57,  H = 7 is the answer

    possibles['H'] = {7}

    # 27ac - WWDD 3 digits starts with 5, W = 16

    possibles['W'] = {16}

