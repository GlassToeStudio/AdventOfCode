''' --- Day 15: Oxygen System ---
Out here in deep space, many things can go wrong. Fortunately, many of those
things have indicator lights. Unfortunately, one of those lights is lit: the
oxygen system for part of the ship has failed!

According to the readouts, the oxygen system must have failed days ago after a
rupture in oxygen tank two; that section of the ship was automatically sealed
once oxygen levels went dangerously low. A single remotely-operated repair
droid is your only option for fixing the oxygen system.

The Elves' care package included an Intcode program (your puzzle input) that
you can use to remotely control the repair droid. By running that program, you
can direct the repair droid to the oxygen system and fix the problem.

The remote control program executes the following steps in a loop forever:

Accept a movement command via an input instruction.
Send the movement command to the repair droid.
Wait for the repair droid to finish the movement operation.
Report on the status of the repair droid via an output instruction.
Only four movement commands are understood: north (1), south (2), west (3),
and east (4). Any other command is invalid. The movements differ in direction,
but not in distance: in a long enough east-west hallway, a series of commands
like 4,4,4,4,3,3,3,3 would leave the repair droid back where it started.

The repair droid can reply with any of the following status codes:

0: The repair droid hit a wall. Its position has not changed.
1: The repair droid has moved one step in the requested direction.
2: The repair droid has moved one step in the requested direction; its new
position is the location of the oxygen system.
You don't know anything about the area around the repair droid, but you can
figure it out by watching the status codes.

For example, we can draw the area using D for the droid, # for walls, . for
locations the droid can traverse, and empty space for unexplored locations.
Then, the initial state looks like this:



   D


To make the droid go north, send it 1. If it replies with 0, you know that
location is a wall and that the droid didn't move:


   #
   D


To move east, send 4; a reply of 1 means the movement was successful:


   #
   .D


Then, perhaps attempts to move north (1), south (2), and east (4) are all met
with replies of 0:


   ##
   .D#
    #

Now, you know the repair droid is in a dead end. Backtrack with 3 (which you
already know will get a reply of 1 because you already know that location is
open):


   ##
   D.#
    #


Then, perhaps west (3) gets a reply of 0, south (2) gets a reply of 1, south
again (2) gets a reply of 0, and then west (3) gets a reply of 2:


   ##
  #..#
  D.#
   #

Now, because of the reply of 2, you know you've found the oxygen system! In
this example, it was only 2 moves away from the repair droid's starting
position.

What is the fewest number of movement commands required to move the repair
droid from its starting position to the location of the oxygen system?
'''

import math
from os import system

GREEN = "\033[0;32;40m"
YELLOW = "\033[0;33;40m"
BLUE = "\033[0;34;40m"
RED = "\033[0;31;40m"
END = "\033[0m"


def clear():
    _ = system('cls')


class Instruction:
    def __init__(self, operation_fn, num_params):
        self.__num_parameters__ = num_params
        self.operation_fn = operation_fn
        self.update_steps(num_params + 1 if num_params > 0 else math.inf)
        self.r = 0

    def get_params(self, intcodes, address):
        p = []
        start = address + 1
        end = start + self.__num_parameters__
        for i in range(start, end):
            p.append(intcodes[i])
        return p

    def update_steps(self, steps):
        self.steps = steps

    def execute(self, intcodes=[],  params=[], modes=[],  address=0):
        self.r = self.operation_fn(
            codes=intcodes, params=params, modes=modes, address=address)
        return self.r


# intcode program helper methods
def format_opcode(opcode):
    ''' Return a string value of the opcode with parameter modes added:

    Notes:
        Opcodes are 5 digits, 2 for the opcode, and 3 for the parameter
        modes. Leading zeros are omitted since these are integers.

        For example, opcode 3 would be 00003
        For example, opcode 103 would be 00103

        ABCDE
         1002

        DE - two-digit opcode,      02 == opcode 2
         C - mode of 1st parameter,  0 == position mode
         B - mode of 2nd parameter,  1 == immediate mode
         A - mode of 3rd parameter,  0 == default

    Args:
        opcode (int): The two digit opcode

    Returns:
        string: Value of the opcode with parameter modes added
    '''

    sopcode = str(opcode)
    length = len(sopcode)
    for i in range(length, 5):
        sopcode = f"{0}{sopcode}"
    return sopcode


def read_full_opcode(opcode):
    ''' Return an integer value of the opcode:

    Notes:
        Opcodes are 5 digits, 2 for the opcode, and 3 for the parameter
        modes. Leading zeros are omitted since these are integers.

        For example, opcode 3 would be 00003
        For example, opcode 103 would be 00103

        ABCDE
         1002

        DE - two-digit opcode,      02 == opcode 2
         C - mode of 1st parameter,  0 == position mode
         B - mode of 2nd parameter,  1 == immediate mode
         A - mode of 3rd parameter,  0 == default

    Args:
        opcode (int): The string version of the opcode with parameter modes

    Returns:
        int: opcode
    '''

    opcode = int(opcode[-2:])
    return opcode


def get_modes(opcode):
    ''' Return an string value of the parameter modes:

    Notes:
        Opcodes are 5 digits, 2 for the opcode, and 3 for the parameter
        modes. Leading zeros are omitted since these are integers.

        For example, opcode 3 would be 00003
        For example, opcode 103 would be 00103

        ABCDE
         1002

        DE - two-digit opcode,      02 == opcode 2
         C - mode of 1st parameter,  0 == position mode
         B - mode of 2nd parameter,  1 == immediate mode
         A - mode of 3rd parameter,  0 == default

    Args:
        opcode (int): The string version of the opcode with parameter modes

    Returns:
        string: parameter modes
    '''

    return opcode[0:3]


# Main helper methods
def get_read_param_by_mode(mode, param, codes):
    ''' Return the values of the given parameters based on their position mode.

    Notes:
        0, position mode, which causes the parameter to be interpreted as a
        position - if the parameter is 50, its value is the value stored
        at address 50 in memory.

        1, immediate mode. In immediate mode, a parameter is interpreted
        as a value - if the parameter is 50, its value is simply 50.

        Parameters that an instruction writes to will never be in immediate
        mode.

    Args:
        mode (int): The parameter mode for the instruction
        param (int): The parameter for the instruction.
        codes (int): The intcode program

    Returns:
        int: paramter based on parameter mode
    '''

    # Position mode: codes[param]
    if mode == '0':
        check_valid_location(codes, param)
        p = codes[param]
    # immediate_mode: param
    elif mode == '1':
        p = param
    # Relative position mode;
    else:
        check_valid_location(codes, relative_base[0] + param)
        p = codes[relative_base[0] + param]
    return p


def get_write_param_by_mode(mode, param, codes):
    ''' Return the values of the given parameters based on their position mode.

    Notes:
        0, position mode, which causes the parameter to be interpreted as a
        position - if the parameter is 50, its value is the value stored
        at address 50 in memory.

        1, immediate mode. In immediate mode, a parameter is interpreted
        as a value - if the parameter is 50, its value is simply 50.

        Parameters that an instruction writes to will never be in immediate
        mode.

    Args:
        mode (int): The parameter mode for the instruction
        param (int): The parameter for the instruction.
        codes (int): The intcode program

    Returns:
        int: paramter based on parameter mode
    '''

    # Position mode: codes[param]
    if mode == '0':
        check_valid_location(codes, param)
        p = param
    # Relative position mode;
    else:
        check_valid_location(codes, relative_base[0] + param)
        p = relative_base[0] + param
    return p


def check_valid_location(codes, param):
    if param >= 0 and codes.get(param, 0) == 0:
        codes[param] = 0


def load_program(intcode):
    program = {}
    for i in range(len(intcode)):
        program[i] = intcode[i]
    return program


def format_data(input):
    return [int(x) for x in input.read().split(',')]


# Operations:
def add_operation(codes, params, modes, **kwargs):
    ''' Adds together numbers read from two positions, params[0] and params[1]
        and stores the result in a third position, params[2].

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction.

    Returns:
        int: opcode instruction 1
    '''

    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    param_2 = get_read_param_by_mode(modes[1], params[1], codes)
    param_3 = get_write_param_by_mode(modes[0], params[2], codes)
    codes[param_3] = param_1 + param_2
    return 1


def mul_operation(codes, params, modes, **kwargs):
    ''' Multiplies together numbers read from two positions, params[0] and
    params[1] and stores the result in a third position, params[2].

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction.

    Returns:
        int: opcode instruction 2
    '''

    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    param_2 = get_read_param_by_mode(modes[1], params[1], codes)
    param_3 = get_write_param_by_mode(modes[0], params[2], codes)
    codes[param_3] = param_1 * param_2
    return 2


def input_operation(codes, params, modes, **kwargs):
    ''' Prompt the user for input and store the value at the given location.

    Notes:
        Takes a single integer as input (from the console) and saves
        it to the position given by its only parameter.
        For example, the instruction 3,50
        would take an input value and store it at address 50.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.

    Returns:
        int: opcode instruction 3
    '''

    user_input = int(input("\t -- Please input a variable: "))
    param_1 = get_write_param_by_mode(modes[2], params[0], codes)
    codes[param_1] = user_input
    return 3


def automated_input_operation(codes, params, modes, **kwargs):
    ''' Modify a value at location in the intcode program with the next
    available value in the input queue.

    Notes:
        Takes a single integer as input (from the input queue) and saves
        it to the position given by its only parameter.
        For example, the instruction 3,50
        would take an input value and store it at address 50.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.

    Returns:
        int: opcode instruction 3
    '''

    param_1 = get_write_param_by_mode(modes[2], params[0], codes)
    codes[param_1] = IO_queue.pop()
    return 3


def output_operation(codes, params, modes, **kwargs):
    ''' Print to the console, the output of the given instruction.

    Notes:
        Outputs the value of its only parameter. (to the console)
        For example, the instruction 4,50 would output the value at
        address 50.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.

    Prints to console:
        the value at the given location

    Returns:
        int: opcode instruction 4
    '''

    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    print(f"\t -- The value is {param_1}")
    return 4


def automated_output_operation(codes, params, modes, **kwargs):
    ''' Add the value from the intcode program at location params[0] to the
    input_queue

    Notes:
        Outputs the value of its only parameter. (to the input queue)
        For example, the instruction 4,50 would output the value at
        address 50.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.

    Returns:
        int: opcode instruction 4
    '''

    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    IO_queue.append(param_1)
    return 4


def jump_if_true_operation(codes, params, modes, address):
    ''' If the first parameter params[0] is non-zero, it sets the instruction
    pointer to the value from the second parameter params[1]. Otherwise,
    it does nothing.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction.

    Returns:
        int: opcode instruction 5
    '''

    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    param_2 = get_read_param_by_mode(modes[1], params[1], codes)

    if param_1 != 0:
        instructions[5].update_steps(param_2 - address)
    else:
        instructions[5].update_steps(len(params) + 1)
    return 5


def jump_if_false_operation(codes, params, modes, address):
    ''' If the first parameter param[0] is zero, it sets the instruction
    pointer to the value from the second parameter params[1].
    Otherwise, it does nothing.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction.

    Returns:
        int: opcode instruction 6
    '''

    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    param_2 = get_read_param_by_mode(modes[1], params[1], codes)

    if param_1 == 0:
        instructions[6].update_steps(param_2 - address)
    else:
        instructions[6].update_steps(len(params) + 1)

    return 6


def less_than_operation(codes, params, modes, **kwargs):
    ''' If the first parameter params[0] is less than the second
    parameter params[1], it stores 1 in the position given by the third
    parameter params[2]. Otherwise, it stores 0.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction.

    Returns:
        int: opcode instruction 7
    '''

    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    param_2 = get_read_param_by_mode(modes[1], params[1], codes)
    param_3 = get_write_param_by_mode(modes[0], params[2], codes)
    if param_1 < param_2:
        codes[param_3] = 1
    else:
        codes[param_3] = 0
    return 7


def equals_operation(codes, params, modes, **kwargs):
    ''' If the first parameter params[0] is equal to the second
    parameter params[1], it stores 1 in the position given by the third
    parameter params[2]. Otherwise, it stores 0. 0.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction.

    Returns:
        int: opcode instruction 8
    '''

    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    param_2 = get_read_param_by_mode(modes[1], params[1], codes)
    if param_1 == param_2:
        if modes[0] == '0':
            codes[params[2]] = 1
        else:
            codes[relative_base[0] + params[2]] = 1
    else:
        if modes[0] == '0':
            codes[params[2]] = 0
        else:
            codes[relative_base[0] + params[2]] = 0
    return 8


def adjust_relative_base(codes, params, modes, **kwargs):
    param_1 = get_read_param_by_mode(modes[2], params[0], codes)
    relative_base[0] = relative_base[0] + param_1
    return


def halt_operation(**kwargs):
    ''' Halts the program.

    Returns:
        int: opcode instruction 99
    '''

    return 99


# Setup
add_instruction = Instruction(add_operation, 3)
mult_instruction = Instruction(mul_operation, 3)
# input_instruction = Instruction(input_operation, 1)
input_instruction = Instruction(automated_input_operation, 1)
# output_instruction = Instruction(output_operation, 1)
output_instruction = Instruction(automated_output_operation, 1)
jump_if_true_instruction = Instruction(jump_if_true_operation, 2)
jump_if_false_instruction = Instruction(jump_if_false_operation, 2)
less_than_instruction = Instruction(less_than_operation, 3)
equals_instruction = Instruction(equals_operation, 3)
adjust_base_instruction = Instruction(adjust_relative_base, 1)
halt_instruction = Instruction(halt_operation, 0)

instructions = {
    1: add_instruction,
    2: mult_instruction,
    3: input_instruction,
    4: output_instruction,
    5: jump_if_true_instruction,
    6: jump_if_false_instruction,
    7: less_than_instruction,
    8: equals_instruction,
    9: adjust_base_instruction,
    99: halt_instruction
}

intcode = []

IO_queue = []
relative_base = [0]


# Main
def run_intcode_program(intcode, current_address, current_amp):
    ''' Run the intcode program ;)

    Args:
        intcode (int[]): the intcode program
        address (int): the starting address for the program
        current_amp (int): Of many, the current program to run

    Returns:
        int: opcode 4 if output received, 99 if halt

    '''

    while (current_address < len(intcode)):
        full_opcode = format_opcode(intcode[current_address])
        opcode = read_full_opcode(full_opcode)
        modes = get_modes(full_opcode)
        params = instructions[opcode].get_params(intcode, current_address)
        r = instructions[opcode].execute(
            intcode,
            params,
            modes,
            current_address
            )
        current_address += instructions[opcode].steps
        yield r
    return r


# Robot
def check_min_max(location, x_min, x_max, y_min, y_max):
    x, y = location
    if x < x_min:
        x_min = x
    if x > x_max:
        x_max = x
    if y < y_min:
        y_min = y
    if y > y_max:
        y_max = y
    return x_min, x_max, y_min, y_max


def turn_right(direction):
    if direction == 4:
        return 2
    if direction == 2:
        return 3
    if direction == 3:
        return 1
    if direction == 1:
        return 4


def turn_left(direction):
    if direction == 4:
        return 1
    if direction == 1:
        return 3
    if direction == 3:
        return 2
    if direction == 2:
        return 4


def populate_map(Maze, x_min, x_max, y_min, y_max):
    clear()
    x_offset = abs(x_min)
    y_offset = abs(y_min)
    x_max += x_offset + 1
    y_max += y_offset + 1

    Map = [[0 for col in range(x_max)] for row in range(y_max)]
    Maze[(0, 0)] = 3
    if not oxygen_location[0] is None:
        Maze[oxygen_location[0]] = 2

    for k in Maze:
        x, y = k
        x += x_offset
        y += y_offset
        Map[y][x] = Maze[k]

    print_map(Map)
    return Map


def print_map(Map):
    fi = open("Day_15/Data/day-15-2.txt", 'w', encoding='utf-8')
    s = ''
    for row in range(len(Map) - 1, -1, -1):
        for col in range(len(Map[0])):
            s += f"{Map[row][col]},"
        s += '\n'
    print(s, file=fi)
    print(s)


def run_robot(intcode):
    i = 0
    track_i = True
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    Maze = {}
    current_direction = 4
    location = (0, 0)
    start_location = (0, 0)
    Maze[location] = 3
    IO_queue.append(4)
    program = load_program(intcode)

    for r in run_intcode_program(program, 0, 0):
        if r == 4 and len(IO_queue) > 0:
            result = IO_queue.pop()

            if result == 0:
                x, y = location
                cx, cy = directions[current_direction]
                Maze[location] = 4

                x_min, x_max, y_min, y_max = check_min_max(
                    (x + cx, y + cy),
                    x_min,
                    x_max,
                    y_min,
                    y_max)

                if (x + cx, y + cy) != oxygen_location[0]:
                    Maze[(x + cx, y + cy)] = 0

                current_direction = turn_left(current_direction)
                IO_queue.append(current_direction)

            elif result == 1:
                x, y = location
                Maze[location] = 1
                cx, cy = directions[current_direction]
                location = (x + cx, y + cy)
                if location not in Maze and track_i:
                    i += 1
                elif track_i:
                    i -= 1
                if location == start_location:
                    return Maze, x_min, x_max, y_min, y_max, i
                x_min, x_max, y_min, y_max = check_min_max(
                    location,
                    x_min,
                    x_max,
                    y_min,
                    y_max)
                if (x + cx, y + cy) != oxygen_location[0]:
                    Maze[location] = 4

                current_direction = turn_right(current_direction)
                IO_queue.append(current_direction)

            elif result == 2:
                i += 1
                track_i = False
                x, y = location
                cx, cy = directions[current_direction]

                location = (x + cx, y + cy)
                oxygen_location[0] = (x + cx, y + cy)

                x_min, x_max, y_min, y_max = check_min_max(
                    location,
                    x_min,
                    x_max,
                    y_min, y_max)

                Maze[location] = 2
                current_direction = turn_right(current_direction)

                IO_queue.append(current_direction)
        pass
    return Maze, x_min, x_max, y_min, y_max, i


Start = RED + '⬤ ' + END,
Wall = '░░',
Success = '  ',
Oxygen = BLUE + '⬤ ' + END,
Me = GREEN + '⬤ ' + END,

tiles = {
    0: Wall,
    1: Success,
    2: Oxygen,
    3: Start,
    4: Me,
}

North = (0, 1)
South = (0, -1)
East = (1, 0)
West = (-1, 0)

directions = {
    1: North,
    2: South,
    3: West,
    4: East
}

oxygen_location = [None]

if __name__ == "__main__":
    with open("Day_15/Data/day-15.txt", "r") as in_file:
        intcode = format_data(in_file)

    Maze, x_min, x_max, y_min, y_max, i = run_robot(intcode)
    Map = populate_map(Maze, x_min, x_max, y_min, y_max)
    print(f"The fewest number of movement commands is {i}")
# Your puzzle answer was 318
