# AdventOfCode
Advent of Code 2019 https://adventofcode.com/2019

## Day 1

<details><summary><b> The Tyranny of the Rocket Equation</b></summary>
<p>
Day 1 is a rather simple problem; calculate the fuel required to cary x amount of mass. You are given an array of masses and an equation to calculate the fuel required based a given mass.
```py
fuel = math.floor(mass / 3) - 2
``` 
Part 1: Easy enough, loop through the array and update the total fuel by using the formula above on each element. Return the sum.

Part 2: You now need to not only calculate the fuel required for the masses, but also the fuel required for the mass of the fuel. Sounds like recursion to me

> *"To understand recursion, you must first understand recursion."*

Loop through the array to calcualate the fuel required, and send that result back through the same formula until the result is 0, updating total fuel and returning the sum.

</p>
</details>

## Day 2

<details><summary><b>1202 Program Alarm </b></summary>
<p>
Day 2 starts on the beggining of a much larger program; an intcode computer. The fist attempt at this computer is rather crude, and not very modular or versitile. It calculates the disired result, but not much else. 

Part 1: You are given an array of integers, the intcode, and must perform one of three operations based on the values of the integers. An 'add', a 'multiply' and a 'halt'. Three hard-coded values are used with some *ifs* to determine what to do. Run the program after changing to integers, as prescribed in the problem, and determine the value at position 0 when it halts. 

Part 2: This problem requires the same intcode computer, but instead of finding the result at position 0 by altering two values, you must dtermine the two values and positions to alter to get a final result in position 0 - kind of backwards.
Much alteration happened to create a brute force method to solve this problem. 

*Not knowing this intcode computer would be used again, the final code is pretty gross.. it does get better though, later.*

</p>
</details>

## Day 3

<details><summary><b>Crossed Wires</b></summary>
<p>
Day 3 provides two wire routings and you must find the intersctiion of wires closest to the origin. I thought creating an image of the the wire diagram was a neat idea, so the code is littered with image manipulation along with the logic...  ¯\\_(ツ)_/¯

Part 1: Draw the diagram and find the intersection closest to the origin. The logic was not the issue.. getting the proper to-scale dimensions for the image was. After that, finding a set of coordiantes in a 'hacky' hash-map proved rather simple. using the 'manhattan distance' formula, we just need to get the x,y combo with the smallest value.

Part 2: Here you had to find the shortest route tp the first intersection. Aka the sum of how far each wire traveled to an intersection. So a short route from wire path one might intersect wire path 2 on a much longer route. 
Crewating a map of all intersections, with their wire routes distance made it quick an easy, if not dirty too. 

</p>
</details>

## Day 4

<details><summary><b>Secure Container</b></summary>
<p>
Cracking a password.. or at least finding the possible solutions in a given range. 

Part 1: Not much here. There are some rules the password must follow, and a range of 6 digit intergers given. Loop those and find all that conform to the rules.

Part 2: Same problem but a few new rules, or modifications to the older rules. Pretty straight forward - with a brute force approach.

</p>
</details>

## Day 5

<details><summary><b>Sunny with a Chance of Asteroids</b></summary>
<p>
**The intcode computer is back.**

Having not realized the intcode computer would return, the previous iteration was basiaclly useless here. A much more elegant solution was created.

Part 1: Serioulsy modify the previous intcode computer with new operations, new rules for paramaters, different amounts of parameters per operation, immediate and positions modes... 🤔

After coming up with an approach, it was all downhill from there. This new intcode computer is easily modifiable, kinda proud of this one.

Two new instructions were added, and the ability to understand parameter modes. Ultimately had to find a diagnostic code output based on a given input of '1'. 

Part 2: No problemo, adding operations to the intcode computer is a breeze. Four more operations added, find another diagnostic output based on a given input of '5'.

</p>
</details>

## Day 6

<details><summary><b>Universal Orbit Map</b></summary>
<p>
Part 1: something something graph, something something search, something something count nodes.

Part 2: Traverse graph from x to y, count steps. 

:P

*Should clarify soon*™
</p>
</details>

## Day 7

<details><summary><b>Amplification Circuit</b></summary>
<p>
Part 1: More intcode, my computer works great! But how it needs to know its own state, and we must run five of them in a sequence, with each prgram output being feed to the next's input. Making the a psuedo yeild opertion, and tracking instruction pointer for each computer helped solve this problem. Get the final output after feeding IO in a sequence, once. 

Part 2: Same as part one, but continuing in a loop intil a halt operation is reached, more tricky than the first part, but doable. I'll realize later that there is an easier way.. although I have yet to make the computer its own class where I can create instances... should have already but meh.

</p>
</details>

## Day 8

<details><summary><b>Space Image Format</b></summary>
<p>
Part 1: Another password. But the elves took a picture this time. The picture is encoded and sent, but we must first verify that the data isnt corrupted. Must find the image layer with the fewest 0 digits. And on that layer, multiply the nuber of 1 digits by the number of 2 dgits. Easy enough, count 0 on every layer, count 1 and 2 on that layer, return the product. 

Part 2: Simply place layer upon layer and read the result. I made a .png.

<p align="center">
<img src="https://github.com/GlassToeStudio/AdventOfCode/blob/master/Day_08/day-8-password.png" width="20%" height="20%"
</p>

</p>
</details>

## Day 9

<details><summary><b>Sensor Boost</b></summary>
<p>
Part 1: More intocde computer changes, add relative mode for instruction pointer. Add ability to 'load into memory' aka the available location for a memeory address can be outside the length of the given intcode. Easy enough to implement. 
Run the program, it outputs a code. 

Part 2:Just provide a new input, read the output. 

</p>
</details>

## Day 10

<details><summary><b>Monitoring Station</b></summary>
<p>
Part 1:
<p align="center">
<img src="https://github.com/GlassToeStudio/AdventOfCode/blob/master/Day_10/asteroid-map-scanning.gif" width="50%" height="50%">
</p>

Part 2:
Solved in python, eventually, but solved in c# in Unity first!
https://github.com/GlassToeStudio/Advent-of-Code-Day-10

</p>
</details>

## Day 11

<details><summary><b>Space Police</b></summary>
<p>
Part 1:
<p align="center">
<img src="https://github.com/GlassToeStudio/AdventOfCode/blob/master/Day_11/day-11-part-1.png" width="50%" height="50%">
</p>


Part 2:
<p align="center">
<img src="https://github.com/GlassToeStudio/AdventOfCode/blob/master/Day_11/day-11-password.png" width="50%" height="50%">
</p>


</p>
</details>