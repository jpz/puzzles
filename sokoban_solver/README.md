# Sokoban Solver

## Intro

This is just a small bit of fun - I was introduced to [Sokoban](https://en.wikipedia.org/wiki/Sokoban) 
by a work colleague, and we had a problem that was bothering us.

My inclination was to write a small program in Python to solve it - this is a simple solution 
using a breadth-first search.  Later as a programming exercise, I re-coded it as a Scala script.

You can run the programs with:

`./sokoban_solver.py level4-map.txt`

or 

`scala -J-Xmx2000m sokoban_solver.scala level4-map.txt`

## Performance:

It's a nice small problem to analyse in terms of performance.  I'm surprised to see Scala 
not be an order of magnitude quicker.  

### Python
```
time ./sokoban_solver.py level4-map.txt
       79.57 real        75.97 user         2.43 sys
```

### Scala
```
time scala -J-Xmx2000m sokoban_solver.scala level4-map.txt
       51.71 real       105.34 user         2.19 sys
```
