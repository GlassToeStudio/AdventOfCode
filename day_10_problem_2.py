''' --- Part Two ---
Once you give them the coordinates, the Elves quickly deploy an Instant
Monitoring Station to the location and discover the worst: there are simply
too many asteroids.

The only solution is complete vaporization by giant laser.

Fortunately, in addition to an asteroid scanner, the new monitoring station
also comes equipped with a giant rotating laser perfect for vaporizing
asteroids. The laser starts by pointing up and always rotates clockwise,
vaporizing any asteroid it hits.

If multiple asteroids are exactly in line with the station, the laser only has
nough power to vaporize one of them before continuing its rotation. In other
words, the same asteroids that can be detected can be vaporized, but if
vaporizing one asteroid makes another one detectable, the newly-detected
asteroid won't be vaporized until the laser has returned to the same position
by rotating a full 360 degrees.

For example, consider the following map, where the asteroid with the new
monitoring station (and laser) is marked X:

    .#....#####...#..
    ##...##.#####..##
    ##...#...#.#####.
    ..#.....X...###..
    ..#.#.....#....##

The first nine asteroids to get vaporized, in order, would be:

    .#....###24...#..
    ##...##.13#67..9#
    ##...#...5.8####.
    ..#.....X...###..
    ..#.#.....#....##

Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7)
won't have a chance to be vaporized until the next full rotation. The laser
continues rotating; the next nine to be vaporized are:

    .#....###.....#..
    ##...##...#.....#
    ##...#......1234.
    ..#.....X...5##..
    ..#.9.....8....76

The next nine to be vaporized are then:

    .8....###.....#..
    56...9#...#.....#
    34...7...........
    ..2.....X....##..
    ..1..............

Finally, the laser completes its first full rotation (1 through 3), a second
rotation (4 through 8), and vaporizes the last asteroid (9) partway through
its third rotation:

    ......234.....6..
    ......1...5.....7
    .................
    ........X....89..
    .................

In the large example above (the one with the best monitoring station location
at 11,13):

--  The 1st asteroid to be vaporized is at 11,12.
--  The 2nd asteroid to be vaporized is at 12,1.
--  The 3rd asteroid to be vaporized is at 12,2.
--  The 10th asteroid to be vaporized is at 12,8.
--  The 20th asteroid to be vaporized is at 16,0.
--  The 50th asteroid to be vaporized is at 16,9.
--  The 100th asteroid to be vaporized is at 10,16.
--  The 199th asteroid to be vaporized is at 9,6.
--  The 200th asteroid to be vaporized is at 8,2.
--  The 201st asteroid to be vaporized is at 10,9.
--  The 299th and final asteroid to be vaporized is at 11,1.

The Elves are placing bets on which will be the 200th asteroid to be vaporized.
Win the bet by determining which asteroid that will be; what do you get if you
multiply its X coordinate by 100 and then add its Y coordinate?
(For example, 8,2 becomes 802.)
'''

import math


data_input = ".#....#.###.........#..##.###.#.....##..............##.......#.#...#...#..#....#.....#....##..##.......#..........###..#.......#....####......#..#.#........#......................##..#....#...##..#...#..#...#....#....#..#.....#.#......#..#...#........#.#....#.#...##.........#...#.......#...##.#.#...#.......#....#........#.........##........#....#..........#.......#....##..........##.....#....#.........#.......#..##......#..#.#.#...#.................#.##.........#...#.#.....#........#....#.#.#.#......#.#...##...#.........##....#.#....#..#.....#.#......##.##...#.......#..#..##.....#..#.........#...##.....#..#.##.#...#.#.#.#.#.#.........#..#...#.##....#.....#......##..#.#..#....#....#####...........#...##...#.....#.......#....#.#.##......#..#..#.#.#....##..#......###.................#..#.#.#....#.....##..#.........#.#.....#..#.......#..#.#............#.#.#.....#..##.....#..#..............#....#.#....##.....#......##..#...#......#..........#..........#.###....#.#...##.#.........##.#..#.....#.#.#......#...##..#.#...#....#...#.#.#.......##.#.........#.#...##.........#............#.#......#....#...#......#.............#.#......#................#...##........#...##......#....#..#..#.....#.#...##.#.#......##...#.#..#...#....##...#.#........#..........##.........#.#.....#.....###.#..#.........#......#......##.#...#.#..#..#.##..............#........##.#..#.#.............#..#.#.........#....##.##..#..#..#.....#...##.#......#....#..#.#....#...###...#.#.......#......#..#...#......##.#..#..#........#....#....#.##.#...#......###.....#.#........##..#.##.###.........#...##.....#..#....#.#............#...#..##..#..##....#.........#..#..#....###..........##..#...#...#..#.."


def is_asteroid(space_map, x, y):
    return '#' in space_map[x][y]


def is_not_me(me_x, me_y, x, y):
    return (x != me_x or y != me_y)


def check_asteroid(space_map, x_from, y_from, x_to, y_to, seen):
    dy = (y_to - y_from)
    dx = (x_to - x_from)
    gcd = math.gcd(dy, dx)
    gcd = gcd * -1 if gcd < 0 else gcd
    val = math.atan2(dy, dx)
    if dy < 0 and dx < 0:
        val += (2 * math.pi)
    dx = dx // gcd
    dy = dy // gcd
    while not is_asteroid(space_map, dx + x_from, dy + y_from):
        dx *= gcd
        dy *= gcd
    seen[val] = (dx + x_from, dy + y_from)


def find_200th_asteroid(seen):
    x_check = 28 # from part 1
    y_check = 29 # from part 1

    for y in range(0, len(space_map)):
        for x in range(0, len(space_map)):
            if is_asteroid(space_map, x, y):
                if is_not_me(x_check, y_check, x, y):
                    check_asteroid(
                        space_map,
                        x_check,
                        y_check,
                        x,
                        y,
                        seen)

    answer = sorted(seen)
    return seen[answer[199]]


def format_output(coords):
    return 100 * coords[0] + coords[1]


size = int(math.sqrt(len(data_input)))
space_map = [[y for y in data_input[x::size]] for x in range(size)]


if __name__ == "__main__":
    seen = {}
    result = find_200th_asteroid(seen)
    print(
        "Coords for 200th asteroid are:",
        result[0], ',',
        result[1], ':', 
        format_output((result[0], result[1])))
# Your puzzle answer was 2628
