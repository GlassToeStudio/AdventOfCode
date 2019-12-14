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

data_input = ".#..#.....#####....#...##"
data_input = "#.#...#.#..###....#..#....#...##.#.#.#.#....#.#.#..##..###.#..#...##....##....##......#....####.###."
data_input = ".#..#..#######.###.#....###.#...###.##.###.##.#.#.....###..#..#.#..#.##..#.#.###.##...##.#.....#.#.."
#data_input = ".#....#.###.........#..##.###.#.....##..............##.......#.#...#...#..#....#.....#....##..##.......#..........###..#.......#....####......#..#.#........#......................##..#....#...##..#...#..#...#....#....#..#.....#.#......#..#...#........#.#....#.#...##.........#...#.......#...##.#.#...#.......#....#........#.........##........#....#..........#.......#....##..........##.....#....#.........#.......#..##......#..#.#.#...#.................#.##.........#...#.#.....#........#....#.#.#.#......#.#...##...#.........##....#.#....#..#.....#.#......##.##...#.......#..#..##.....#..#.........#...##.....#..#.##.#...#.#.#.#.#.#.........#..#...#.##....#.....#......##..#.#..#....#....#####...........#...##...#.....#.......#....#.#.##......#..#..#.#.#....##..#......###.................#..#.#.#....#.....##..#.........#.#.....#..#.......#..#.#............#.#.#.....#..##.....#..#..............#....#.#....##.....#......##..#...#......#..........#..........#.###....#.#...##.#.........##.#..#.....#.#.#......#...##..#.#...#....#...#.#.#.......##.#.........#.#...##.........#............#.#......#....#...#......#.............#.#......#................#...##........#...##......#....#..#..#.....#.#...##.#.#......##...#.#..#...#....##...#.#........#..........##.........#.#.....#.....###.#..#.........#......#......##.#...#.#..#..#.##..............#........##.#..#.#.............#..#.#.........#....##.##..#..#..#.....#...##.#......#....#..#.#....#...###...#.#.......#......#..#...#......##.#..#..#........#....#....#.##.#...#......###.....#.#........##..#.##.###.........#...##.....#..#....#.#............#...#..##..#..##....#.........#..#..#....###..........##..#...#...#..#.."


def count_occurences(arr, num):
    count = Counter(arr)
    return count[num]


def print_map(space_map, char):
    for y in range(len(space_map)):
        for x in range(len(space_map)):
            print(space_map[x][y], end=char)
        print('\n')


def check_x_axis(space_map, x, y, asteroid):
    ans1 = 0
    ans2 = 0
    # # print('x', x)
    for i in range(x - 1, 0, -1):
        # # print(i)
        #space_map[i][y] = red_start + "#" + end_color
        if '#' in space_map[i][y]:
            # # print('x, y', i, y)
            if ans1 < 1:
                # space_map[i][y] = green_start + "#" + end_color
                ans1 += 1
    # # print('\n')
    for i in range(x+1, len(space_map)):
        # # print(i)
        #space_map[i][y] = red_start + "#" + end_color
        if '#' in space_map[i][y]:
            # # print('x, y', i, y)
            if ans2 < 1:
                # space_map[i][y] = green_start + "#" + end_color
                ans2 += 1
    # # print("Count", min(ans1, 1), min(ans2, 1))
    return min(ans1, 1) + min(ans2, 1)


def check_y_axis(space_map, x, y, asteroid):
    ans1 = 0
    ans2 = 0
    # # print('y', y)
    for i in range(y - 1, 0, -1):
        # # print(i)
        # space_map[x][i] = red_start + "#" + end_color
        if '#' in space_map[x][i]:
            # # print('x, y', x, i)
            if ans1 < 1:
                # space_map[x][i] = green_start + "#" + end_color
                ans1 += 1
    for i in range(y + 1, len(space_map)):
        # # print(i)
        # space_map[x][i] = red_start + "#" + end_color
        if '#' in space_map[x][i]:
            # # print('x, y', x, i)
            if ans2 < 1:
                # space_map[x][i] = green_start + "#" + end_color
                ans2 += 1
    # # print("Count", min(ans1, 1), min(ans2, 1))
    return min(ans1, 1) + min(ans2, 1)


def check_diagonals(space_map, x_from, y_from, x_to, y_to, asteroid):
    # check x and y in seen
    #print(f"For x and y: {x_to},{y_to}")
    top = y_to - y_from
    bottom = x_to - x_from
    m = (top) / (bottom)
    b = y_from - m * x_from
    ## print("Top and bottom:", top, bottom)
    ## print(f"Slope and intercetp: {m}, {b}")

    if (m, b) in slope_checked[asteroid]:
        # print("Seen")
        return 0
    else:
        slope_checked[asteroid].append((m, b))

    # space_map[x_to][y_to] = green_start + "#" + end_color
    return 1


green_start = "\033[0;32;40m"
yellow_start = "\033[0;33;40m"
blue_start = "\033[0;34;40m"
end_color = "\033[0m"
red_start = "\033[0;31;40m"

size = int(math.sqrt(len(data_input)))
space_map = [[y for y in data_input[x::size]] for x in range(size)]
num_asteroids = count_occurences(data_input, '#')
slope_checked = [[] for x in range(num_asteroids)]
total_seen = [[0 for y in range(size)] for x in range(size)]
asteroid_index = -1
max_asteroid = 0
coords = (0, 0)

# For every location in the map
for asteroid_y in range(len(space_map)):
    for asteroid_x in range(len(space_map)):
        # This is an asteroid, check all the asteroid it can see
        #space_map[asteroid_x][asteroid_y] = yellow_start + '#' + end_color
        if '#' in space_map[asteroid_x][asteroid_y]:
            asteroid_index += 1
            if(asteroid_index >= len(slope_checked)):
                print("*", asteroid_index)
            # Look along its X axis
            total_seen[asteroid_x][asteroid_y] += check_x_axis(space_map,
                                                               asteroid_x,
                                                               asteroid_y,
                                                               asteroid_index)
            # Look along its Y axis
            total_seen[asteroid_x][asteroid_y] += check_y_axis(space_map,
                                                               asteroid_x,
                                                               asteroid_y,
                                                               asteroid_index)
            #print_map(space_map, ' ')
            slope_checked[asteroid_index].clear()
            # Check every other asteroid
            for y_forward in range(asteroid_y + 1, len(space_map)):
                for x_forward in range(asteroid_x + 1, len(space_map)):
                    #print(x_forward, y_forward)
                    # If this location is an asteroid, check if we can see it
                    if '#' in space_map[x_forward][y_forward]:
                        # space_map[x_forward][y_forward] = blue_start + '#' + end_color
                        #print(f"-X and Y From {asteroid_x}, {asteroid_y}")
                        total_seen[asteroid_x][asteroid_y] += check_diagonals(
                            space_map, asteroid_x, asteroid_y, x_forward,
                            y_forward, asteroid_index)
            #print_map(space_map, ' ')
            slope_checked[asteroid_index].clear()
            for y_backward in range(asteroid_y - 1, -1, -1):
                for x_backward in range(asteroid_x - 1, -1, -1):
                    #print(x_backward, y_backward)
                    # If this location is an asteroid, check if we can see it
                    if '#' in space_map[x_backward][y_backward]:
                        # space_map[x_backward][y_backward] = blue_start + '#' + end_color
                        #print(f"X and Y From {asteroid_x}, {asteroid_y}")
                        total_seen[asteroid_x][asteroid_y] += check_diagonals(
                            space_map, asteroid_x, asteroid_y, x_backward,
                            y_backward, asteroid_index)
            #print_map(space_map, ' ')
            slope_checked[asteroid_index].clear()
            for y_backward in range(asteroid_y - 1, -1, -1):
                for x_forward in range(asteroid_x + 1, len(space_map)):
                    #print('*', x_forward, y_backward)
                    # If this location is an asteroid, check if we can see it
                    if '#' in space_map[x_forward][y_backward]:
                        # space_map[x_forward][y_backward] = blue_start + '#' + end_color
                        #print(f"X and Y From {asteroid_x}, {asteroid_y}")
                        total_seen[asteroid_x][asteroid_y] += check_diagonals(
                            space_map, asteroid_x, asteroid_y, x_forward,
                            y_backward, asteroid_index)
            #print_map(space_map, ' ')
            slope_checked[asteroid_index].clear()
            for y_forward in range(asteroid_y + 1, len(space_map)):
                for x_backward in range(asteroid_x - 1, -1, -1):
                    #print("-", x_backward, y_forward)
                    # If this location is an asteroid, check if we can see it
                    if '#' in space_map[x_backward][y_forward]:
                        # space_map[x_backward][y_forward] = blue_start + '#' + end_color
                        #print(f"X and Y From {asteroid_x}, {asteroid_y}")
                        total_seen[asteroid_x][asteroid_y] += check_diagonals(
                            space_map, asteroid_x, asteroid_y, x_backward,
                            y_forward, asteroid_index)

            if total_seen[asteroid_x][asteroid_y] > max_asteroid:
                max_asteroid = total_seen[asteroid_x][asteroid_y]
                coords = (asteroid_x, asteroid_y)
                
print_map(space_map, ' ')
print_map(total_seen, ', ')
print("*", asteroid_index)
print("Max value is:", max_asteroid, "Coords are:", coords)
