''' --- Day 10: Monitoring Station ---
You fly into the asteroid belt and reach the Ceres monitoring station. The
Elves here have an emergency: they're having trouble tracking all of the
asteroids and can't be sure they're safe.

The Elves would like to build a new monitoring station in a nearby area of
space; they hand you a map of all of the asteroids in that region (your puzzle
input).

The map indicates whether each position is empty (.) or contains an asteroid
(#). The asteroids are much smaller than they appear on the map, and every
asteroid is exactly in the center of its marked position. The asteroids can be
described with X,Y coordinates where X is the distance from the left edge and
Y is the distance from the top edge (so the top-left corner is 0,0 and the
position immediately to its right is 1,0).

Your job is to figure out which asteroid would be the best place to build a
new monitoring station. A monitoring station can detect any asteroid to which
it has direct line of sight - that is, there cannot be another asteroid
exactly between them. This line of sight can be at any angle, not just lines
aligned to the grid or diagonally. The best location is the asteroid that can
detect the largest number of other asteroids.

For example, consider the following map:

    .#..#
    .....
    #####
    ....#
    ...##

The best location for a new monitoring station on this map is the highlighted
asteroid at 3,4 because it can detect 8 asteroids, more than any other
location. (The only asteroid it cannot detect is the one at 1,0; its view of
this asteroid is blocked by the asteroid at 2,2.) All other asteroids are
worse locations; they can detect 7 or fewer other asteroids. Here is the
number of other asteroids a monitoring station on each asteroid could detect:

    .7..7
    .....
    67775
    ....7
    ...87

Here is an asteroid (#) and some examples of the ways its line of sight might
be blocked. If there were another asteroid at the location of a capital letter,
the locations marked with the corresponding lowercase letter would be blocked
and could not be detected:

    #.........
    ...A......
    ...B..a...
    .EDCG....a
    ..F.c.b...
    .....c....
    ..efd.c.gb
    .......c..
    ....f...c.
    ...e..d..c

Here are some larger examples:

Best is 5,8 with 33 other asteroids detected:

    ......#.#.
    #..#.#....
    ..#######.
    .#.#.###..
    .#..#.....
    ..#....#.#
    #..#....#.
    .##.#..###
    ##...#..#.
    .#....####

Best is 1,2 with 35 other asteroids detected:

    #.#...#.#.
    .###....#.
    .#....#...
    ##.#.#.#.#
    ....#.#.#.
    .##..###.#
    ..#...##..
    ..##....##
    ......#...
    .####.###.

Best is 6,3 with 41 other asteroids detected:

    .#..#..###
    ####.###.#
    ....###.#.
    ..###.##.#
    ##.##.#.#.
    ....###..#
    ..#.#..#.#
    #..#.#.###
    .##...##.#
    .....#.#..

Best is 11,13 with 210 other asteroids detected:

    .#..##.###...#######
    ##.############..##.
    .#.######.########.#
    .###.#######.####.#.
    #####.##.#.##.###.##
    ..#####..#.#########
    ####################
    #.####....###.#.#.##
    ##.#################
    #####.##.###..####..
    ..######..##.#######
    ####.##.####...##..#
    .#####..#.######.###
    ##...#.##########...
    #.##########.#######
    .####.#.###.###.#.##
    ....##.##.###..#####
    .#.#.###########.###
    #.#.#.#####.####.###
    ###.##.####.##.#..##

Find the best location for a new monitoring station. How many other asteroids
can be detected from that location?
'''
import math
from collections import Counter

GREEN = "\033[0;32;40m"
YELLOW = "\033[0;33;40m"
BLUE = "\033[0;34;40m"
RED = "\033[0;31;40m"
END = "\033[0m"

data_input = ".#..#.....#####....#...##"
data_input = "#.#...#.#..###....#..#....#...##.#.#.#.#....#.#.#..##..###.#..#...##....##....##......#....####.###."
data_input = ".#..#..#######.###.#....###.#...###.##.###.##.#.#.....###..#..#.#..#.##..#.#.###.##...##.#.....#.#.."
data_input = ".#....#.###.........#..##.###.#.....##..............##.......#.#...#...#..#....#.....#....##..##.......#..........###..#.......#....####......#..#.#........#......................##..#....#...##..#...#..#...#....#....#..#.....#.#......#..#...#........#.#....#.#...##.........#...#.......#...##.#.#...#.......#....#........#.........##........#....#..........#.......#....##..........##.....#....#.........#.......#..##......#..#.#.#...#.................#.##.........#...#.#.....#........#....#.#.#.#......#.#...##...#.........##....#.#....#..#.....#.#......##.##...#.......#..#..##.....#..#.........#...##.....#..#.##.#...#.#.#.#.#.#.........#..#...#.##....#.....#......##..#.#..#....#....#####...........#...##...#.....#.......#....#.#.##......#..#..#.#.#....##..#......###.................#..#.#.#....#.....##..#.........#.#.....#..#.......#..#.#............#.#.#.....#..##.....#..#..............#....#.#....##.....#......##..#...#......#..........#..........#.###....#.#...##.#.........##.#..#.....#.#.#......#...##..#.#...#....#...#.#.#.......##.#.........#.#...##.........#............#.#......#....#...#......#.............#.#......#................#...##........#...##......#....#..#..#.....#.#...##.#.#......##...#.#..#...#....##...#.#........#..........##.........#.#.....#.....###.#..#.........#......#......##.#...#.#..#..#.##..............#........##.#..#.#.............#..#.#.........#....##.##..#..#..#.....#...##.#......#....#..#.#....#...###...#.#.......#......#..#...#......##.#..#..#........#....#....#.##.#...#......###.....#.#........##..#.##.###.........#...##.....#..#....#.#............#...#..##..#..##....#.........#..#..#....###..........##..#...#...#..#.."


def count_occurences(arr, num):
    count = Counter(arr)
    return count[num]


def print_map(space_map, char):
    for y in range(len(space_map)):
        for x in range(len(space_map)):
            print(space_map[x][y], end=char)
        print('\n')


def check_x_axis(space_map, x, y, do_color):
    ans1 = 0
    ans2 = 0
    for i in range(x - 1, 0, -1):
        if is_asteroid(space_map, i, y):
            color_asteroid(space_map, i, y, GREEN, do_color)
            ans1 += 1
            break
    for i in range(x+1, len(space_map)):
        if is_asteroid(space_map, i, y):
            color_asteroid(space_map, i, y, GREEN, do_color)
            ans2 += 1
            break
    return min(ans1, 1) + min(ans2, 1)


def check_y_axis(space_map, x, y, do_color):
    ans1 = 0
    ans2 = 0
    for i in range(y - 1, 0, -1):
        if is_asteroid(space_map, x, i):
            color_asteroid(space_map, x, i, GREEN, do_color)
            ans1 += 1
            break
    for i in range(y + 1, len(space_map)):
        if is_asteroid(space_map, x, i):
            color_asteroid(space_map, x, i, GREEN, do_color)
            ans2 += 1
            break
    return min(ans1, 1) + min(ans2, 1)


def check_diagonals(space_map, x_from, y_from, x_to, y_to, asteroid, do_color):
    m = (y_to - y_from) / (x_to - x_from)
    b = y_from - m * x_from

    if (m, b) in slope_checked[asteroid]:
        return 0
    else:
        slope_checked[asteroid].append((m, b))
        color_asteroid(space_map, x_to, y_to, GREEN, do_color)
    return 1


def is_asteroid(space_map, x, y):
    return '#' in space_map[x][y]


def color_asteroid(_map, x, y, color, do_color, char='#'):
    if do_color:
        _map[x][y] = color + str(char) + END


def find_best_station(x_start, x_end, y_start, y_end, do_color):
    asteroid_index = -1
    max_check = 0
    coords = (0, 0)
    # For every location in the map
    for y_check in range(y_start, y_end):
        for x_check in range(x_start, x_end):
            # This is an asteroid, check all the asteroid it can see
            color_asteroid(space_map, x_check, y_check, RED, do_color)
            if is_asteroid(space_map, x_check, y_check):
                asteroid_index += 1
                # Look along its X axis
                total_seen[x_check][y_check] += check_x_axis(space_map,
                                                             x_check,
                                                             y_check,
                                                             do_color)
                # Look along its Y axis
                total_seen[x_check][y_check] += check_y_axis(space_map,
                                                             x_check,
                                                             y_check,
                                                             do_color)

                slope_checked[asteroid_index].clear()
                for y in range(y_check + 1, len(space_map)):
                    for x in range(x_check + 1, len(space_map)):
                        if is_asteroid(space_map, x, y):
                            total_seen[x_check][y_check] += check_diagonals(
                                space_map, x_check, y_check, x,
                                y, asteroid_index, do_color)

                slope_checked[asteroid_index].clear()
                for y in range(y_check - 1, -1, -1):
                    for x in range(x_check + 1, len(space_map)):
                        if is_asteroid(space_map, x, y):
                            total_seen[x_check][y_check] += check_diagonals(
                                space_map, x_check, y_check, x,
                                y, asteroid_index, do_color)

                slope_checked[asteroid_index].clear()
                for y in range(y_check - 1, -1, -1):
                    for x in range(x_check - 1, -1, -1):
                        if is_asteroid(space_map, x, y):
                            total_seen[x_check][y_check] += check_diagonals(
                                space_map, x_check, y_check, x,
                                y, asteroid_index, do_color)

                slope_checked[asteroid_index].clear()
                for y in range(y_check + 1, len(space_map)):
                    for x in range(x_check - 1, -1, -1):
                        if is_asteroid(space_map, x, y):
                            total_seen[x_check][y_check] += check_diagonals(
                                space_map, x_check, y_check, x,
                                y, asteroid_index, do_color)

                if total_seen[x_check][y_check] > max_check:
                    max_check = total_seen[x_check][y_check]
                    coords = (x_check, y_check)

    return max_check, coords


size = int(math.sqrt(len(data_input)))
space_map = [[y for y in data_input[x::size]] for x in range(size)]
num_asteroids = count_occurences(data_input, '#')
slope_checked = [[] for x in range(num_asteroids)]
total_seen = [[0 for y in range(size)] for x in range(size)]


if __name__ == "__main__":
    max_check, coords = find_best_station(0, len(space_map),
                                          0, len(space_map), False)

    find_best_station(coords[0], coords[0] + 1,
                      coords[1], coords[1] + 1, True)
    color_asteroid(total_seen, coords[0], coords[1], GREEN, True, max_check)
    print_map(total_seen, ', ')
    print_map(space_map, '  ')
    print("Max value is:", max_check, "Coords are:", coords)
# Your puzzle answer was 340
