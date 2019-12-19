'''
--- Day 12: The N-Body Problem ---
The space near Jupiter is not a very safe place; you need to be careful of a
big distracting red spot, extreme radiation, and a whole lot of moons swirling
around. You decide to start by tracking the four largest moons: Io, Europa,
Ganymede, and Callisto.

After a brief scan, you calculate the position of each moon
(your puzzle input).
You just need to simulate their motion so you can avoid them.

Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional
velocity. The position of each moon is given in your scan; the x, y, and z
velocity of each moon starts at 0.

Simulate the motion of the moons in time steps. Within each time step, first
update the velocity of every moon by applying gravity. Then, once all moons'
velocities have been updated, update the position of every moon by applying
velocity. Time progresses by one step once all of the positions are updated.

To apply gravity, consider every pair of moons. On each axis (x, y, and z),
the velocity of each moon changes by exactly +1 or -1 to pull the moons
together. For example, if Ganymede has an x position of 3, and Callisto has a
x position of 5, then Ganymede's x velocity changes by +1 (because 5 > 3) and
Callisto's x velocity changes by -1 (because 3 < 5). However, if the positions
on a given axis are the same, the velocity on that axis does not change for
that pair of moons.

Once all gravity has been applied, apply velocity: simply add the velocity of
each moon to its own position. For example, if Europa has a position of
x=1, y=2, z=3 and a velocity of x=-2, y=0,z=3, then its new position would be
x=-1, y=2, z=6. This process does not modify the velocity of any moon.

For example, suppose your scan reveals the following positions:

    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>

Simulating the motion of these moons would produce the following:

    After 0 steps:
    pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
    pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
    pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
    pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>

    After 1 step:
    pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
    pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
    pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
    pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>

    After 2 steps:
    pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
    pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
    pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
    pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>

    After 3 steps:
    pos=<x= 5, y=-6, z=-1>, vel=<x= 0, y=-3, z= 0>
    pos=<x= 0, y= 0, z= 6>, vel=<x=-1, y= 2, z= 4>
    pos=<x= 2, y= 1, z=-5>, vel=<x= 1, y= 5, z=-4>
    pos=<x= 1, y=-8, z= 2>, vel=<x= 0, y=-4, z= 0>

    After 4 steps:
    pos=<x= 2, y=-8, z= 0>, vel=<x=-3, y=-2, z= 1>
    pos=<x= 2, y= 1, z= 7>, vel=<x= 2, y= 1, z= 1>
    pos=<x= 2, y= 3, z=-6>, vel=<x= 0, y= 2, z=-1>
    pos=<x= 2, y=-9, z= 1>, vel=<x= 1, y=-1, z=-1>

    After 5 steps:
    pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>
    pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>
    pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>
    pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>

    After 6 steps:
    pos=<x=-1, y=-7, z= 3>, vel=<x= 0, y= 2, z= 1>
    pos=<x= 3, y= 0, z= 0>, vel=<x=-1, y=-1, z=-5>
    pos=<x= 3, y=-2, z= 1>, vel=<x= 1, y=-4, z= 5>
    pos=<x= 3, y=-4, z=-2>, vel=<x= 0, y= 3, z=-1>

    After 7 steps:
    pos=<x= 2, y=-2, z= 1>, vel=<x= 3, y= 5, z=-2>
    pos=<x= 1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>
    pos=<x= 3, y=-7, z= 5>, vel=<x= 0, y=-5, z= 4>
    pos=<x= 2, y= 0, z= 0>, vel=<x=-1, y= 4, z= 2>

    After 8 steps:
    pos=<x= 5, y= 2, z=-2>, vel=<x= 3, y= 4, z=-3>
    pos=<x= 2, y=-7, z=-5>, vel=<x= 1, y=-3, z=-1>
    pos=<x= 0, y=-9, z= 6>, vel=<x=-3, y=-2, z= 1>
    pos=<x= 1, y= 1, z= 3>, vel=<x=-1, y= 1, z= 3>

    After 9 steps:
    pos=<x= 5, y= 3, z=-4>, vel=<x= 0, y= 1, z=-2>
    pos=<x= 2, y=-9, z=-3>, vel=<x= 0, y=-2, z= 2>
    pos=<x= 0, y=-8, z= 4>, vel=<x= 0, y= 1, z=-2>
    pos=<x= 1, y= 1, z= 5>, vel=<x= 0, y= 0, z= 2>

    After 10 steps:
    pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
    pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
    pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
    pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>

Then, it might help to calculate the total energy in the system. The total
energy for a single moon is its potential energy multiplied by its kinetic
energy. A moon's potential energy is the sum of the absolute values of its
x, y, and z position coordinates. A moon's kinetic energy is the sum of the
absolute values of its velocity coordinates. Below, each line shows the
calculations for a moon's potential energy (pot), kinetic energy (kin), and
total energy:

    Energy after 10 steps:
    pot: 2 + 1 + 3 =  6;   kin: 3 + 2 + 1 = 6;   total:  6 * 6 = 36
    pot: 1 + 8 + 0 =  9;   kin: 1 + 1 + 3 = 5;   total:  9 * 5 = 45
    pot: 3 + 6 + 1 = 10;   kin: 3 + 2 + 3 = 8;   total: 10 * 8 = 80
    pot: 2 + 0 + 4 =  6;   kin: 1 + 1 + 1 = 3;   total:  6 * 3 = 18
    Sum of total energy: 36 + 45 + 80 + 18 = 179

In the above example, adding together the total energy for all moons after 10
steps produces the total energy in the system, 179.

Here's a second example:

    <x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>

Every ten steps of simulation for 100 steps produces:

    After 0 steps:
    pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>

    After 10 steps:
    pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
    pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
    pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
    pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>

    After 20 steps:
    pos=<x=-10, y=  3, z= -4>, vel=<x= -5, y=  2, z=  0>
    pos=<x=  5, y=-25, z=  6>, vel=<x=  1, y=  1, z= -4>
    pos=<x= 13, y=  1, z=  1>, vel=<x=  5, y= -2, z=  2>
    pos=<x=  0, y=  1, z=  7>, vel=<x= -1, y= -1, z=  2>

    After 30 steps:
    pos=<x= 15, y= -6, z= -9>, vel=<x= -5, y=  4, z=  0>
    pos=<x= -4, y=-11, z=  3>, vel=<x= -3, y=-10, z=  0>
    pos=<x=  0, y= -1, z= 11>, vel=<x=  7, y=  4, z=  3>
    pos=<x= -3, y= -2, z=  5>, vel=<x=  1, y=  2, z= -3>

    After 40 steps:
    pos=<x= 14, y=-12, z= -4>, vel=<x= 11, y=  3, z=  0>
    pos=<x= -1, y= 18, z=  8>, vel=<x= -5, y=  2, z=  3>
    pos=<x= -5, y=-14, z=  8>, vel=<x=  1, y= -2, z=  0>
    pos=<x=  0, y=-12, z= -2>, vel=<x= -7, y= -3, z= -3>

    After 50 steps:
    pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>
    pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>
    pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>
    pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>

    After 60 steps:
    pos=<x= 36, y=-10, z=  6>, vel=<x=  5, y=  0, z=  3>
    pos=<x=-18, y= 10, z=  9>, vel=<x= -3, y= -7, z=  5>
    pos=<x=  8, y=-12, z= -3>, vel=<x= -2, y=  1, z= -7>
    pos=<x=-18, y= -8, z= -2>, vel=<x=  0, y=  6, z= -1>

    After 70 steps:
    pos=<x=-33, y= -6, z=  5>, vel=<x= -5, y= -4, z=  7>
    pos=<x= 13, y= -9, z=  2>, vel=<x= -2, y= 11, z=  3>
    pos=<x= 11, y= -8, z=  2>, vel=<x=  8, y= -6, z= -7>
    pos=<x= 17, y=  3, z=  1>, vel=<x= -1, y= -1, z= -3>

    After 80 steps:
    pos=<x= 30, y= -8, z=  3>, vel=<x=  3, y=  3, z=  0>
    pos=<x= -2, y= -4, z=  0>, vel=<x=  4, y=-13, z=  2>
    pos=<x=-18, y= -7, z= 15>, vel=<x= -8, y=  2, z= -2>
    pos=<x= -2, y= -1, z= -8>, vel=<x=  1, y=  8, z=  0>

    After 90 steps:
    pos=<x=-25, y= -1, z=  4>, vel=<x=  1, y= -3, z=  4>
    pos=<x=  2, y= -9, z=  0>, vel=<x= -3, y= 13, z= -1>
    pos=<x= 32, y= -8, z= 14>, vel=<x=  5, y= -4, z=  6>
    pos=<x= -1, y= -2, z= -8>, vel=<x= -3, y= -6, z= -9>

    After 100 steps:
    pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
    pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
    pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
    pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>

    Energy after 100 steps:
    pot:  8 + 12 +  9 = 29;   kin: 7 +  3 + 0 = 10;   total: 29 * 10 = 290
    pot: 13 + 16 +  3 = 32;   kin: 3 + 11 + 5 = 19;   total: 32 * 19 = 608
    pot: 29 + 11 +  1 = 41;   kin: 3 +  7 + 4 = 14;   total: 41 * 14 = 574
    pot: 16 + 13 + 23 = 52;   kin: 7 +  1 + 1 =  9;   total: 52 *  9 = 468
    Sum of total energy: 290 + 608 + 574 + 468 = 1940

What is the total energy in the system after simulating the moons given in
your scan for 1000 steps?
'''
import math


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def values(self):
        return (self.x, self.y, self.z)


class Moon:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector(0, 0, 0)
        self.kinetic_energy = 0
        self.potential_energy = 0
        self.__update_kinetic_energy__()
        self.__update_potential_energy__()
        self.initial_state = (position.x, position.y, position.z)

    def update_velocity(self, moon_position):
        self.velocity.x += self.__update_velocity__(self.position.x,
                                                    moon_position.x)
        self.velocity.y += self.__update_velocity__(self.position.y,
                                                    moon_position.y)
        self.velocity.z += self.__update_velocity__(self.position.z,
                                                    moon_position.z)

    def update_position(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z
        self.__update_kinetic_energy__()
        self.__update_potential_energy__()

    def get_total_energy(self):
        return self.kinetic_energy * self.potential_energy

    def output(self):
        return (
            f"pos=<{self.position.x}, {self.position.y}, {self.position.z}>, "
            f"vel=<{self.velocity.x}, {self.velocity.y}, {self.velocity.z}>")

    def __update_velocity__(self, me, them):
        if me < them:
            return 1
        elif me > them:
            return -1
        else:
            return 0

    def __update_kinetic_energy__(self):
        self.kinetic_energy = (
            abs(self.position.x) +
            abs(self.position.y) +
            abs(self.position.z))

    def __update_potential_energy__(self):
        self.potential_energy = (
            abs(self.velocity.x) +
            abs(self.velocity.y) +
            abs(self.velocity.z))


def apply_gravity(moons):
    for moon in moons:
        for othermoon in moons:
            if moon is not othermoon:
                moon.update_velocity(othermoon.position)


def apply_velocity(moons):
    for moon in moons:
        moon.update_position()


def get_output(moons):
    for moon in moons:
        print(moon.output())
    print('\n')


def format_input(input):
    output = []
    s = input.strip('\n').strip().split('>')
    for line in s:
        line = line.strip()
        if len(line) > 0:
            ss = line.strip()[1:].split(',')
            x = int(ss[0].split('=')[1])
            y = int(ss[1].split('=')[1])
            z = int(ss[2].split('=')[1])
            output.append(Vector(x, y, z))
    return output


def LCM(a, b):
    lcm = a * b // math.gcd(a, b)
    return lcm


def check_axis(axis):
    for i in range(len(moons)):
        if (moons[i].position.values()[axis] != moons[i].initial_state[axis] or
                moons[i].velocity.values()[axis] != 0):
            return False
    return True


input = "<x=3, y=3, z=0><x=4, y=-16, z=2><x=-10, y=-6, z=5><x=-3, y=0, z=-13>"

if __name__ == "__main__":
    out = format_input(input)

    Io = Moon(out[0])
    Europa = Moon(out[1])
    Ganymede = Moon(out[2])
    Callisto = Moon(out[3])

    axis_periods = {}
    moons = [Io, Europa, Ganymede, Callisto]

    steps = 0
    count = 0
    while count < 3:
        apply_gravity(moons)
        apply_velocity(moons)
        steps += 1
        if 'x' not in axis_periods:
            if check_axis(0):
                axis_periods['x'] = steps
                count += 1
        if 'y' not in axis_periods:
            if check_axis(1):
                axis_periods['y'] = steps
                count += 1
        if 'z' not in axis_periods:
            if check_axis(2):
                axis_periods['z'] = steps
                count += 1

    universe_period = LCM(axis_periods['x'], axis_periods['y'])
    universe_period = LCM(universe_period, axis_periods['z'])


print("The number of simulations required "
      f"to reach the intial state is {universe_period}")
# Your puzzle answer was 380635029877596
