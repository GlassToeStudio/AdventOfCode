''' --- Part Two ---
During the second Go / No Go poll, the Elf in charge of the Rocket Equation
Double-Checker stops the launch sequence. Apparently, you forgot to include
additional fuel for the fuel you just added.

Fuel itself requires fuel just like a module - take its mass, divide by three,
round down, and subtract 2. However, that fuel also requires fuel, and that
fuel requires fuel, and so on. Any mass that would require negative fuel
should instead be treated as if it requires zero fuel; the remaining mass,
if any, is instead handled by wishing really hard, which has no mass and is
outside the scope of this calculation.

So, for each module mass, calculate its fuel and add it to the total.
Then, treat the fuel amount you just calculated as the input mass and repeat
the process, continuing until a fuel requirement is zero or negative.
For example:

    - A module of mass 14 requires 2 fuel. This fuel requires no further fuel
        (2 divided by 3 and rounded down is 0, which would call for a
        negative fuel), so the total fuel required is still just 2.
    - At first, a module of mass 1969 requires 654 fuel. Then, this fuel
        requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel,
        which requires 21 fuel, which requires 5 fuel, which requires no
        further fuel. So, the total fuel required for a module of mass 1969
        is 654 + 216 + 70 + 21 + 5 = 966.
    - The fuel required by a module of mass 100756 and its fuel is:
    33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.

What is the sum of the fuel requirements for all of the modules on your
spacecraft when also taking into account the mass of the added fuel?
(Calculate the fuel requirements for each module separately, then add them all
up at the end.)
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


def calculate_fuel_recursive(mass):
    ''' Return total fuel required for a given mass.

    Notes:
        The fuel required for a given mass, has its own mass
        and therefore has its own fuel requirements. Recursively
        calculate the total fuel required for a given mass,
        along with the mass of the fuel itself.

    Args:
        mass (int): The mass to be evaluated.

    Returns:
        (int) The fuel required for the given mass.
    '''

    fuel = calculate_fuel(mass)
    if fuel >= 0:
        fuel += calculate_fuel_recursive(fuel)
    else:
        fuel = 0

    return fuel


if __name__ == "__main__":
    total = 0
    for mass in modules:
        total += calculate_fuel_recursive(mass)

    print(f"Total fuel required for problem 2: {total}")
# Your puzzle answer was 4898972
