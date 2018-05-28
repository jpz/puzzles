#!/usr/bin/env swipl

:- set_prolog_flag(verbose, silent).
:- initialization time(puzzlerun(_)).
:- use_module(library(clpfd)).

e10(1, N) :- N#=1.
e10(2, N) :- N#=10.
e10(3, N) :- N#=100.
e10(4, N) :- N#=1000.
e10(5, N) :- N#=10000.


% compare the nth digit of two numbers, the least significant digit being 1 (i.e. one-base indexe)
digitsame(Number1, Digit1, Number2, Digit2) :-
	e10(Digit1, Div1),
	e10(Digit2, Div2),
	N1 #= Number1//Div1 mod 10,
	N2 #= Number2//Div2 mod 10,
	N1 #= N2.

% build a list of squares
squares_under(1, [1]).
squares_under(S, [S|Ss]) :- Sminus1 is S-1, _D*_D #= S, squares_under(Sminus1, Ss), !.
squares_under(S, Ss) :- Sminus1 is S-1, squares_under(Sminus1, Ss).

% build a list of cubes
cubes_under(1, [1]).
cubes_under(S, [S|Ss]) :- Sminus1 is S-1, _D*_D*_D #= S, cubes_under(Sminus1, Ss), !.
cubes_under(S, Ss) :- Sminus1 is S-1, cubes_under(Sminus1, Ss).

% generic helper which converts list to clpfd domain
list_to_domain([H|T], H\/TDomain) :- list_to_domain(T, TDomain).
list_to_domain([H], H..H).

% build list of palindromes

reverse_number(Num, Reverse) :- reverse_number(Num, Reverse, 0).
reverse_number(0, Accum, Accum).
reverse_number(Num, Reverse, Accum) :- Num #\= 0, NumDiv10 #= Num div 10, AccumNew #= Accum*10+(Num mod 10), reverse_number(NumDiv10, Reverse, AccumNew).

is_palindrome(N) :- reverse_number(N, Reverse), N = Reverse.

palindromes_under(N, Palindromes) :- findall(X, (between(1,N,X), is_palindrome(X)), Palindromes).

% build list of primes
is_divisible(Number, [Divisor|_Divisors]) :-
        (Number mod Divisor) =:= 0, !.
is_divisible(Number, [Divisor|Divisors]) :-
        Divisor*Divisor =< Number, is_divisible(Number, Divisors).
is_divisible(Number, [Divisor]) :-
        (Number mod Divisor) =:= 0.

prime_list(1, []) :- !.
prime_list(2, [2]) :- !.
prime_list(N, List) :- Nminus1 is N-1, prime_list(Nminus1, ListMinus1),
        (is_divisible(N, ListMinus1), List = ListMinus1, !; append(ListMinus1, [N], List), !).


% domain definitions from list definitions above
squares(Domain) :- squares_under(100000, Squares), list_to_domain(Squares, Domain).
cubes(Domain) :- cubes_under(100000, Cubes), list_to_domain(Cubes, Domain).
primes(Domain) :- prime_list(100000, List), list_to_domain(List, Domain).
palindromes(Domain) :- palindromes_under(100000, Palindromes), list_to_domain(Palindromes, Domain).

% digit sum
digit_sum(N, N) :- N #< 10.
digit_sum(N, Sum) :- N #>= 10, Rest #= N//10, digit_sum(Rest, Sum2), Sum #= (N mod 10) + Sum2.

has_factor(N, Factor) :- (N mod Factor) #= 0.

% 42 clues to guess
puzzle(Answers) :-
	squares(Squares),
	cubes(Cubes),
	palindromes(Palindromes),
	primes(Primes),
	NotSquares = \(Squares),
	NotCubes = \(Cubes),
	NotPalindromes = \(Palindromes),
	NotPrimes = \(Primes),
	Answers = [A1,A2,A3,A4,A5,A6,
		A7,A8,A9,A10,A11,A12,
		A13,A14,A15,A16,A17,A18,
		A19,A20,A21,A22,A23,A24,
		A25,A26,A27,A28,A29,A30,
		A31,A32,A33,A34,A35,A36,
		A37,A38,A39,A40,A41,A42],
	[A2,A40] ins 10..99,
	[A3,A5,A7,A10,A11,A13,A14,A15,A17,A19,A26,A27,A30,A32,A34,A35,A36,A38,A39,A41] ins 100..999,
	[A4,A8,A9,A12,A18,A20,A28,A29,A31,A37] ins 1000..9999,
	[A1,A6,A16,A21,A22,A23,A24,A25,A33,A42] ins 10000..99999,
	% only 1,4,9,16,25,36 are perfect squares
	[A1,A4,A9,A16,A25,A36] ins Squares,
	[A2,A3,A5,A6,A7,A8,A10,A11,A12,A13,A14,A15,A17,A18,A19,A20,A21,A22,A23,A24,A26,A27,A28,A29,A30,A31,A32,A33,A34,A35,A37,A38,A39,A40,A41,A42] ins NotSquares,
	% only 1,8,27 are perfect cubes
	[A1,A8,A27] ins Cubes,
	[A2,A3,A4,A5,A6,A7,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,A23,A24,A25,A26,A28,A29,A30,A31,A32,A33,A34,A35,A36,A37,A38,A39,A40,A41,A42] ins NotCubes,
	% only 2,3,5,7,11,13,17,19,23,29,31,37,41 are prime numbers
	[A2,A3,A5,A7,A11,A13,A17,A19,A23,A29,A31,A37,A41] ins Primes,
	[A1,A4,A6,A8,A9,A10,A12,A14,A15,A16,A18,A20,A21,A22,A24,A25,A26,A27,A28,A30,A32,A33,A34,A35,A36,A38,A39,A40,A42] ins NotPrimes,
	% only 11,22,33 are palindromes
	[A11, A22, A33] ins Palindromes,
	[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A23,A24,A25,A26,A27,A28,A29,A30,A31,A32,A34,A35,A36,A37,A38,A39,A40,A41,A42] ins NotPalindromes,
	%% digit_sum of 2 is even
	digit_sum(A2, DS2), has_factor(DS2, 2),
	% and 2 is a factor of 14, 22, 30
	has_factor(A14, A2),
	has_factor(A22, A2),
	has_factor(A30, A2),
	% 5 < 7 < 13 < 19
	chain([A5, A7, A13, A19], #<),
	% and 5 is a factor of 15
	has_factor(A15, A5),
	% 6 = 3 * 2
	A6 #= A3 * A2,
	% 7 is a factor of 28 
	has_factor(A28, A7),
	% 9 is a factor of 18 
	has_factor(A18, A9),
	% 12 = 4 + 3 + 3 + 2
	A12 #= A4 + A3 + A3 + A2,
	% 13 is a factor of 26 and 39
	has_factor(A26, A13),
	has_factor(A39, A13),
	% 14 reversed is a prime number greater than 3
	reverse_number(A14, R14), R14 in Primes, R14 #> A3,	
	% The digit sum of 17 > the digit sum of 15
	digit_sum(A17, DS17), digit_sum(A15, DS15), DS17 #> DS15,
	% 20 = 10 + 10
	A20 #= A10 + A10,
	% 20 + 21 < 42
	A20 + A21 #< A42,
	% The digit sum of 21 plus the digit sum of 31 = the digit sum of 12 + the digit sum of 40
	digit_sum(A21, DS21), digit_sum(A31, DS31), digit_sum(A12, DS12), digit_sum(A40, DS40), DS21 + DS31 #= DS12 + DS40,
	% The digit sum of 23 plus the digit sum of 30 = the digit sum of 17
	digit_sum(A23, DS23), digit_sum(A30, DS30), digit_sum(A17, DS17), DS23 + DS30 #= DS17,
	% 23 reversed > 23
	reverse_number(A23, R23), R23 #> A23,	
	% 24 = 12 + 12
	A24 #= A12 + A12,
	% The digit sum of 29 = the digit sum of 38
	digit_sum(A29, DS29), digit_sum(A38, DS38), DS29 #= DS38,
	% The digit sum of 31 = the digit sum of 13
	digit_sum(A13, DS13), DS31 #= DS13,
	% The digit sum of 32 = the digit sum of 14
	digit_sum(A32, DS32), digit_sum(A14, DS14), DS32 #= DS14,
	% The digit sum of 33 = twice the digit sum of 30
	digit_sum(A33, DS33), DS33 #= 2 * DS30,
	% 34 = 37 - 3
	A34 #= A37 - A3,
	% The digit sum of 34 = the digit sum of 16 > the digit sum of 10
	digit_sum(A34, DS34), digit_sum(A16, DS16), digit_sum(A10, DS10), DS34 #= DS16, DS16 #> DS10,
	% The digit sum of 35 = the digit sum of 26
	digit_sum(A35, DS35), digit_sum(A26, DS26), DS35 #= DS26,
	% 38 = 19 + 19
	A38 #= A19 + A19,
	% The digit sum of 41 > the digit sum of 40
	digit_sum(A41, DS41), digit_sum(A40, DS40), DS41 #> DS40,
	% 42 = 24 + 15 + 3
	A42 #= A24 + A15 + A3,
	all_distinct(Answers),
	digitsame(A1,4,A2,2),
	digitsame(A1,3,A3,3),
	digitsame(A1,1,A4,4),
	digitsame(A7,2,A8,4),
	digitsame(A7,1,A9,4),
	digitsame(A10,2,A2,1),
	digitsame(A10,1,A3,2),
	digitsame(A11,2,A4,3),
	digitsame(A11,1,A5,2),
	digitsame(A12,4,A6,4),
	digitsame(A12,2,A8,3),
	digitsame(A12,1,A9,3),
	digitsame(A14,2,A3,1),
	digitsame(A14,1,A15,3),
	digitsame(A16,5,A5,1),
	digitsame(A16,4,A6,3),
	digitsame(A16,2,A8,2),
	digitsame(A16,1,A9,2),
	digitsame(A17,3,A13,2),
	digitsame(A17,1,A18,4),
	digitsame(A19,3,A15,2),
	digitsame(A19,2,A4,1),
	digitsame(A21,5,A13,1),
	digitsame(A21,3,A18,3),
	digitsame(A21,2,A15,1),
	digitsame(A22,4,A6,1),
	digitsame(A22,3,A20,3),
	digitsame(A23,3,A18,2),
	digitsame(A23,2,A24,5),
	digitsame(A25,4,A26,3),
	digitsame(A25,3,A20,2),
	digitsame(A25,1,A27,3),
	digitsame(A30,2,A31,4),
	digitsame(A30,1,A26,2),
	digitsame(A32,3,A20,1),
	digitsame(A32,1,A27,2),
	digitsame(A33,5,A28,3),
	digitsame(A33,4,A29,3),
	digitsame(A33,2,A24,3),
	digitsame(A33,1,A34,3),
	digitsame(A35,3,A26,1),
	digitsame(A35,2,A36,3),
	digitsame(A37,4,A28,2),
	digitsame(A37,3,A29,2),
	digitsame(A37,1,A24,2),
	digitsame(A38,3,A34,2),
	digitsame(A38,2,A31,2),
	digitsame(A39,3,A36,2),
	digitsame(A39,2,A40,2),
	digitsame(A41,3,A28,1),
	digitsame(A41,2,A29,1),
	digitsame(A42,5,A31,1),
	digitsame(A42,3,A36,1),
	digitsame(A42,2,A40,1).


puzzlerun(Answers) :- puzzle(Answers), labeling([ff], Answers), print(Answers).


