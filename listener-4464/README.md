# Listener 4464

This is a bit of further work on constraint propagation, this time using SWI-Prolog
and its CLP(FD) module (constraint propagation over integers) to specify the problem.

I wrote this just to test whether this would actually work, and I was pleased it does
find the answer - however it does appear to be rather brute force.  In some of my other 
bespoke written constraint problem solvers I had started to look at pairwise distributions, 
as it seems to reduce the dimensionality a lot, which I've not implemented in with this 
approach, which ends up trying around 5 billion inferences and taking around 10 mins
on my workstation.

Another aspect of writing this was that it was extremely difficult to enter the code
correctly, or spot where a typo had occurred.  I thus at some stage (in frustration) reverted
to typing in the solution from (here)[https://www.listenercrossword.com/Solutions/S2017/Notes_4464.html)
and validating, before removing the rules, and seeing it produced the answer.

```
?- time(puzzlerun(Answers)).
[15625,59,631,5776,139,37229,241,4913,1764,893,373,7097,271,118,834,92416,773,3528,367,1786,13549,89798,11213,14194,48841,813,125,7712,6143,531,3331,622,71217,778,327,256,1409,734,542,45,239,15659]
% 5,382,046,128 inferences, 475.806 CPU in 479.079 seconds (99% CPU, 11311434 Lips)
```
