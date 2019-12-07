''' --- Day 1: The Tyranny of the Rocket Equation ---
Santa has become stranded at the edge of the Solar System while delivering
presents to other planets! To accurately calculate his position in space,
safely align his warp drive, and return to Earth in time to save Christmas,
he needs you to bring him measurements from fifty stars.

Collect stars by solving puzzles. Two puzzles will be made available on each
day in the Advent calendar; the second puzzle is unlocked when you complete
the first. Each puzzle grants one star. Good luck!

The Elves quickly load you into a spacecraft and prepare to launch.

At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper.
They haven't determined the amount of fuel required yet.

Fuel required to launch a given module is based on its mass. Specifically, to
find the fuel required for a module, take its mass, divide by three, round
down, and subtract 2.

For example:

For a mass of 12, divide by 3 and round down to get 4,
then subtract 2 to get 2.
For a mass of 14, dividing by 3 and rounding down still yields 4,
o the fuel required is also 2.
For a mass of 1969, the fuel required is 654.
For a mass of 100756, the fuel required is 33583.
The Fuel Counter-Upper needs to know the total fuel requirement.
To find it,individually calculate the fuel needed for the mass of each module
(your puzzle input), then add together all the fuel values.

What is the sum of the fuel requirements for all of the modules on your
spacecraft?
'''

import math

modules = [
    99603, 121503, 86996, 72052, 112039, 106616, 123581, 123171, 52480, 68686,
    66395, 102661, 110250, 73289, 105725, 123802, 75488, 79426, 98634, 76095,
    50852, 141405, 112388, 72180, 103300, 124602, 104531, 94751, 63270, 139027,
    145939, 62275, 91812, 74751, 144010, 60221, 62821, 51080, 149802, 53067,
    102574, 131339, 78942, 88430, 105314, 72764, 55214, 79095, 97458, 68699,
    106974, 141492, 57673, 141866, 139355, 134222, 52145, 83293, 144322, 70741,
    107873, 123638, 141011, 133249, 99065, 120480, 100767, 136550, 147323,
    146988, 65583, 141287, 53097, 50662, 121124, 94886, 59344, 93981, 112492,
    149136, 56647, 96430, 63968, 117987, 138475, 125958, 74967, 64480, 104644,
    70273, 50671, 147116, 147101, 89096, 94697, 83282, 74533, 68418, 145578,
    59032
]


def calculate_fuel(mass):
    ''' Calculate the fuel needed for the given mass.

    Args:
        mass (int): the mass to be evaluated.

    Returns:
        int: the fuel required for the given mass.
    '''

    return (math.floor(mass / 3) - 2)


total = 0
for mass in modules:
    total += calculate_fuel(mass)

print(f"Total fuel required for problem 1: {total}")
# Your puzzle answer was 3267890
