''' --- Part Two ---
All this drifting around in space makes you wonder about the nature of the
universe. Does history really repeat itself? You're curious whether the moons
will ever return to a previous state.

Determine the number of steps that must occur before all of the moons'
positions and velocities exactly match a previous point in time.

For example, the first example above takes 2772 steps before they exactly
match a previous point in time; it eventually returns to the initial state:

    After 0 steps:
    pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

    After 2770 steps:
    pos=<x=  2, y= -1, z=  1>, vel=<x= -3, y=  2, z=  2>
    pos=<x=  3, y= -7, z= -4>, vel=<x=  2, y= -5, z= -6>
    pos=<x=  1, y= -7, z=  5>, vel=<x=  0, y= -3, z=  6>
    pos=<x=  2, y=  2, z=  0>, vel=<x=  1, y=  6, z= -2>

    After 2771 steps:
    pos=<x= -1, y=  0, z=  2>, vel=<x= -3, y=  1, z=  1>
    pos=<x=  2, y=-10, z= -7>, vel=<x= -1, y= -3, z= -3>
    pos=<x=  4, y= -8, z=  8>, vel=<x=  3, y= -1, z=  3>
    pos=<x=  3, y=  5, z= -1>, vel=<x=  1, y=  3, z= -1>

    After 2772 steps:
    pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

Of course, the universe might last for a very long time before repeating.
Here's a copy of the second example from above:

    <x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>

This set of initial positions takes 4686774924 steps before it repeats a
previous state! Clearly, you might need to find a more efficient way to
simulate the universe.

How many steps does it take to reach the first state that exactly matches a
previous state?
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
