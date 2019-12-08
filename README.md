# AdventOfCode
Advent of Code 2019 https://adventofcode.com/2019

## Day 1

Day 1 is a rather simple problem; calculate the fuel required to cary x amount of mass. You are given an array of masses and an equation to calculate the fuel required based a given mass.
```py
fuel = math.floor(mass / 3) - 2
``` 
Part 1: Easy enough, loop through the array and update the total fuel by using the formula above on each element. Return the sum.

Part 2: You now need to not only calculate the fuel required for the masses, but also the fuel required for the mass of the fuel. Sounds like recursion to me

> *"To understand recursion, you must first understand recursion."*

Loop through the array to calcualate the fuel required, and send that result back through the same formula until the result is 0, updating total fuel and returning the sum.

## Day 2

Day 2 starts on the beggining of a much larger program; an intcode computer. The fist attempt at this computer is rather crude, and not very modular or versitile. It calculates the disired result, but not much else. 

Part 1: You are given an array of integers, the intcode, and must perform one of three operations based on the values of the integers. An 'add', a 'multiply' and a 'halt'. Three hard-coded values are used with some *ifs* to determine what to do. Run the program after changing to integers, as prescribed in the problem, and determine the value at position 0 when it halts. 

Part 2: This problem requires the same intcode computer, but instead of finding the result at position 0 by altering two values, you must dtermine the two values and positions to alter to get a final result in position 0 - kind of backwards.
Much alteration happened to create a brute force method to solve this problem. 

*Not knowing this intcode computer would be used again, the final code is pretty gross.. it does get better though, later.*

## Day 3

Day 3 provides two wire routings and you must find the intersctiion of wires closest to the origin. I thought creating an image of the the wire diagram was a neat idea, so the code is littered with image manipulation along with the logic...  ¯\\_(ツ)_/¯

Part 1: Draw the diagram and find the intersection closest to the origin. The logic was not the issue.. getting the proper to-scale dimensions for the image was. After that, finding a set of coordiantes in a 'hacky' hash-map proved rather simple. using the 'manhattan distance' formula, we just need to get the x,y combo with the smallest value.

Part 2: Here you had to find the shortest route tp the first intersection. Aka the sum of how far each wire traveled to an intersection. So a short route from wire path one might intersect wire path 2 on a much longer route. 
Crewating a map of all intersections, with their wire routes distance made it quick an easy, if not dirty too. 

# Day 4

Cracking a password.. or at least finding the possible solutions in a given range. 

Part 1: Not much here. There are some rules the password must follow, and a range of 6 digit intergers given. Loop those and find all that conform to the rules.

Part 2: Same problem but a few new rules, or modifications to the older rules. Pretty straight forward - with a brute force approach.

# Day 5

**The intcode computer is back.**

Having not realized the intcode computer would return, the previous iteration was basiaclly useless here. A much more elegant solution was created.

Part 1: Serioulsy modify the previous intcode computer with new operations, new rules for paramaters, different amounts of parameters per operation, immediate and positions modes... 🤔

After coming up with an approach, it was all downhill from there. This new intcode computer is easily modifiable, kinda proud of this one.

Two new instructions were added, and the ability to understand parameter modes. Ultimately had to find a diagnostic code output based on a given input of '1'. 

Part 2: No problemo, adding operations to the intcode computer is a breeze. Four more operations added, find another diagnostic output based on a given input of '5'.

# Day 6

tbd
