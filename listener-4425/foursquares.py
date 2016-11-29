#!/usr/bin/env python3

##################################
# PUBLIC INTERFACE
##################################

# This file implements a dictionary of the sum of square solutions for n, where
#  n = a^2 + b^2 + c^2 + d^2, and a to d are rangebound from [0..25], and a >= b >= c >= d
# A solution is determined according to precedence rules which favours a minimum number
# of squares when there are two solutions, i.e. d, c, or b = 0, and thereafter, larger leading numbers,
# e.g. 18 = 3^2 + 3^2 = 4^2 + 1^2 + 1^2, however [3 3 0 0] is the solution for 18 due to fewer digits required.
# 55 = 5^2 + 5^2 + 2^2 1^2 = 7^2 + 2^2 + 1^2 + 1^2, however [7 2 1 1] is preferred due to larger leading numbers (7 > 5)


def get_foursquare(num):
    return FOURSQUARES.get(num)


def get_foursquare_inv(nums):
    return get_foursquare(sum_of_squares(nums))


def is_foursquare(nums):
    nums = _regularise_numbers(nums)
    return get_foursquare_inv(nums) == nums


##################################
# IMPLEMENTATION
##################################

FOURSQUARES = {}


def _regularise_numbers(numbers: list):
    """sorts the numbers descending, and removes all zeros"""
    nums = numbers.copy()
    ok = True
    while ok:
        try:
            nums.remove(0)
        except:
            ok = False
    nums.sort(reverse=True)
    return nums


def sum_of_squares(lst: list):
    return sum(n * n for n in lst)


def _init():
    for i in range(26):
        for j in range(26):
            for k in range(26):
                for l in range(26):
                    nums = _regularise_numbers([i, j, k, l])
                    total = sum_of_squares(nums)
                    if total in FOURSQUARES:
                        old = FOURSQUARES[total]
                        if len(nums) < len(old):
                            FOURSQUARES[total] = nums
                        elif len(nums) == len(old) and nums > old:
                            FOURSQUARES[total] = nums
                    else:
                        FOURSQUARES[total] = nums

_init()

