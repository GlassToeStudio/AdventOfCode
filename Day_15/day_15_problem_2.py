''' --- Part Two ---
You quickly repair the oxygen system; oxygen gradually fills the area.

Oxygen starts in the location containing the repaired oxygen system. It takes
one minute for oxygen to spread to all open locations that are adjacent to a
location that already contains oxygen. Diagonal locations are not adjacent.

In the example above, suppose you've used the droid to explore the area fully
and have the following map (where locations that currently contain oxygen are
marked O):

 ##
#..##
#.#..#
#.O.#
 ###

Initially, the only location which contains oxygen is the location of the
repaired oxygen system. However, after one minute, the oxygen spreads to all
open (.) locations that are adjacent to a location containing oxygen:

 ##
#..##
#.#..#
#OOO#
 ###

After a total of two minutes, the map looks like this:

 ##
#..##
#O#O.#
#OOO#
 ###

After a total of three minutes:

 ##
#O.##
#O#OO#
#OOO#
 ###

And finally, the whole region is full of oxygen after a total of four minutes:

 ##
#OO##
#O#OO#
#OOO#
 ###

So, in this example, all locations contain oxygen after 4 minutes.

Use the repair droid to get a complete map of the area. How many minutes will
it take to fill with oxygen?
'''

import math
import PIL
from PIL import Image
from os import system

GREEN = "\033[0;32;40m"
YELLOW = "\033[0;33;40m"
BLUE = "\033[0;34;40m"
RED = "\033[0;31;40m"
END = "\033[0m"


def clear():
    _ = system('cls')


def format_data(in_file):
    Map = []
    for line in in_file:
        line = line.rstrip().strip()[:-1]
        Map.append([int(x) for x in line.split(',')])
    return Map
# Robot


def print_map(Map):
    clear()
    # fi = open("Day_15/maze-oxygen.txt", 'w', encoding='utf-8')
    s = ''
    for row in range(len(Map) - 1, -1, -1):
        for col in range(len(Map[0])):
            s += f"{tiles[Map[row][col]][0]}"
        s += '\n'
    # print(s, file=fi)
    print(s)


def create_map_image(Map, pixels, img, index):
    for x in range(len(Map)):
        for y in range(len(Map[0])):
            if Map[x][y] == 0:
                pixels[y, x] = (165, 73, 42)
            elif Map[x][y] == 1:
                pixels[y, x] = (0, 0, 0)
            elif Map[x][y] == 2 or Map[x][y] == 5:
                pixels[y, x] = (42, 134, 165)
            elif Map[x][y] == 3:
                pixels[y, x] = (255, 0, 0)
            elif Map[x][y] == 4:
                pixels[y, x] = (0, 255, 0)
            else:
                pixels[y, x] = (0, 0, 0)
    img.save(f'Day_15/Images/maze_oxygen-{index}.png')
    return pixels, img


def find_oxygen_start(Maze):
    for x in range(len(Maze)):
        for y in range(len(Maze[0])):
            if Maze[x][y] == 2:
                return (x, y)


def fill_oxygen(Maze, start):
    # width = len(Maze)
    # height = len(Maze[0])
    # img = Image.new('RGB', (width, height), color='black')
    # pixels = img.load()
    # index = 0

    x, y = start
    next_oxygen = [(x, y)]
    minutes = 0
    while len(next_oxygen) > 0:
        temp = []
        for o in next_oxygen:
            r, c = o
            if Maze[r+1][c] == 1:
                Maze[r+1][c] = 5
                temp.append((r+1, c))
            if Maze[r-1][c] == 1:
                Maze[r-1][c] = 5
                temp.append((r-1, c))
            if Maze[r][c-1] == 1:
                Maze[r][c-1] = 5
                temp.append((r, c-1))
            if Maze[r][c+1] == 1:
                Maze[r][c+1] = 5
                temp.append((r, c+1))
        if len(temp) > 0:
            minutes += 1
        next_oxygen = temp
        # pixels, img = create_map_image(Maze, pixels, img, index)
        # index += 1
        # print_map(Maze)
    return minutes  # , pixels, img, index


Start = RED + '⬤ ' + END,
Wall = '░░',
Success = '  ',
Oxygen = BLUE + '⬤ ' + END,
Me = GREEN + '⬤ ' + END,
Oxygen_path = BLUE + '██' + END,

tiles = {
    0: Wall,
    1: Success,
    2: Oxygen,
    3: Start,
    4: Me,
    5: Oxygen_path,
}


if __name__ == "__main__":
    with open("Day_15/Data/day-15-2.txt", "r") as in_file:
        Maze = format_data(in_file)
    x, y = find_oxygen_start(Maze)
    minutes = fill_oxygen(Maze, (x, y))
    # minutes, pixels, img, index = fill_oxygen(Maze, (x, y))
    Map = print_map(Maze)
    # pixels, img = create_map_image(Maze, pixels, img, index)
    print(f"It will take {minutes} minutes to fill with oxygen.")
# Your puzzle answer was 390
