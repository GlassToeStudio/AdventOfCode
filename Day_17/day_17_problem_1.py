''' --- Day 17: Set and Forget ---
An early warning system detects an incoming solar flare and automatically
activates the ship's electromagnetic shield. Unfortunately, this has cut off
the Wi-Fi for many small robots that, unaware of the impending danger, are now
trapped on exterior scaffolding on the unsafe side of the shield. To rescue
them, you'll have to act quickly!

The only tools at your disposal are some wired cameras and a small vacuum
robot currently asleep at its charging station. The video quality is poor, but
the vacuum robot has a needlessly bright LED that makes it easy to spot no
matter where it is.

An Intcode program, the Aft Scaffolding Control and Information Interface
(ASCII, your puzzle input), provides access to the cameras and the vacuum
robot. Currently, because the vacuum robot is asleep, you can only access the
cameras.

Running the ASCII program on your Intcode computer will provide the current
view of the scaffolds. This is output, purely coincidentally, as ASCII code:
35 means #, 46 means ., 10 starts a new line of output below the current one,
and so on. (Within a line, characters are drawn left-to-right.)

In the camera output, # represents a scaffold and . represents open space. The
vacuum robot is visible as ^, v, <, or > depending on whether it is facing up,
down, left, or right respectively. When drawn like this, the vacuum robot is
always on a scaffold; if the vacuum robot ever walks off of a scaffold and
begins tumbling through space uncontrollably, it will instead be visible as X.

In general, the scaffold forms a path, but it sometimes loops back onto itself.
For example, suppose you can see the following view from the cameras:

..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..

Here, the vacuum robot, ^ is facing up and sitting at one end of the scaffold
near the bottom-right of the image. The scaffold continues up, loops across
itself several times, and ends at the top-left of the image.

The first step is to calibrate the cameras by getting the alignment parameters
of some well-defined points. Locate all scaffold intersections; for each, its
alignment parameter is the distance between its left edge and the left edge of
the view multiplied by the distance between its top edge and the top edge of
the view. Here, the intersections from the above image are marked O:

..#..........
..#..........
##O####...###
#.#...#...#.#
##O###O###O##
..#...#...#..
..#####...^..

For these intersections:

--  The top-left intersection is 2 units from the left of the image and 2
    units from the top of the image, so its alignment parameter is 2 * 2 = 4.
--  The bottom-left intersection is 2 units from the left and 4 units from the
    top, so its alignment parameter is 2 * 4 = 8.
--  The bottom-middle intersection is 6 from the left and 4 from the top, so
    its alignment parameter is 24.
--  The bottom-right intersection's alignment parameter is 40.
--  To calibrate the cameras, you need the sum of the alignment parameters. In
    the above example, this is 76.

Run your ASCII program. What is the sum of the alignment parameters for the
scaffold intersections?
'''

from Computer.computer import Int_Computer


def format_data(data):
    return [int(x) for x in data.read().split(',')]


def find_intersections(Map, Scaffold):
    intersections = []
    for r in range(len(Map)):
        for c in range(len(Map[0])):
            if Map[r][c] == Scaffold:
                if r != 0 and c != 0 and r != len(Map) - 1 and c != len(Map[0]) - 1:
                    if Map[r-1][c] == Scaffold and \
                        Map[r+1][c] == Scaffold and \
                        Map[r][c-1] == Scaffold and \
                        Map[r][c+1] == Scaffold:
                            intersections.append((r, c))
    return intersections


def calibrate_cameras(intersections):
    sum = 0
    for intersection in intersections:
        sum += intersection[0] * intersection[1]
    return sum


def print_map(Map):
    # fi = open("Day_17/Data/day-17-2.txt", 'w', encoding='utf-8')
    s = ''
    for row in range(len(Map)):
        for col in range(len(Map[0])):
            s += f"{Map[row][col]}"
        s += '\n'
    # print(s, file=fi)
    print(s)


def run_robot(intcode):
    Maze = []
    temp = []
    computer = Int_Computer(intcode, output_to_queue=True)
    for _ in computer.run():
        if len(computer.IO_queue) > 0:
            t = computer.IO_queue.pop()
            if t != 10:
                temp.append(tiles[t])
            elif len(temp) > 0:
                Maze.append(temp)
                temp = []

    intersections = find_intersections(Maze, Scaffold)

    return Maze, intersections


Scaffold = '░░'
Space = '  '
Up = '^ '

tiles = {
    35: Scaffold,
    46: Space,
    94: Up
}


if __name__ == "__main__":
    with open("Day_17/Data/day-17.txt", "r") as in_file:
        intcode = format_data(in_file)

    Maze, intersections = run_robot(intcode)
    sum = calibrate_cameras(intersections)
    print(f'The sum of the alignment parameters for the scaffold intersections is {sum}.')
    # Your puzzle answer was 14332
