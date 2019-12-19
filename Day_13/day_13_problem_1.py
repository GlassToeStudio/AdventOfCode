''' --- Day 13: Care Package ---
As you ponder the solitude of space and the ever-increasing three-hour
roundtrip for messages between you and Earth, you notice that the Space Mail
Indicator Light is blinking. To help keep you sane, the Elves have sent you a
care package.

It's a new game for the ship's arcade cabinet! Unfortunately, the arcade is
all the way on the other end of the ship. Surely, it won't be hard to build
your own - the care package even comes with schematics.

The arcade cabinet runs Intcode software like the game the Elves sent (your
puzzle input). It has a primitive screen capable of drawing square tiles on a
grid. The software draws tiles to the screen with output instructions: every
three output instructions specify the x position (distance from the left), y
position (distance from the top), and tile id. The tile id is interpreted as
follows:

--  0 is an empty tile. No game object appears in this tile.
--  1 is a wall tile. Walls are indestructible barriers.
--  2 is a block tile. Blocks can be broken by the ball.
--  3 is a horizontal paddle tile. The paddle is indestructible.
--  4 is a ball tile. The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a
horizontal paddle tile (1 tile from the left and 2 tiles from the top) and a
ball tile (6 tiles from the left and 5 tiles from the top).

Start the game. How many block tiles are on the screen when the game exits?
'''


import math
from os import system, name


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


def get_read_param_by_mode(mode, param, codes):
    ''' Return the values of the given parameters based on their position mode.

    Notes:
        0, position mode, which causes the parameter to be interpreted as a
        position - if the parameter is 50, its value is the value stored
        at address 50 in memory.

        1, immediate mode. In immediate mode, a parameter is interpreted
        as a value - if the parameter is 50, its value is simply 50.

        Parameters that an instruction writes to will never be in immediate mode.

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

        Parameters that an instruction writes to will never be in immediate mode.

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


# Main helper methods
def get_copy_of_program(intcode):
    ''' Return a copy of the intcode.

    Args:
        intcode (int[]): The intcode program

    Returns:
        int[]: copy of intcode
    '''

    program = []
    for i in intcode:
        program.append(i)
    return program


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
input_instruction = Instruction(input_operation, 1)
#input_instruction = Instruction(automated_input_operation, 1)
#output_instruction = Instruction(output_operation, 1)
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


IO_queue = []
instruction_queue = []
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


def print_board(board):
    # i = open("Day_13/board.txt", 'w', encoding='utf-8')
    b = ''
    for y in range(len(board)):
        for x in range(len(board[0])):
            b += board[y][x]
        b+='\n'
    #print(b, file=fi)
    print(b)


GREEN = "\033[0;32;40m"
YELLOW = "\033[0;33;40m"
BLUE = "\033[0;34;40m"
RED = "\033[0;31;40m"
END = "\033[0m"

tiles = {
    0: ' ',
    1: BLUE + '█' + END,
    2: GREEN + '░' + END,
    3: YELLOW + '-' + END,
    4: RED + '©' + END
}

intcode = []
if __name__ == "__main__":
    with open("Day_13/Data/day-13.txt", "r") as in_file:
        intcode = format_data(in_file)

    program = load_program(intcode)
    board = [[' ' for x in range(45)] for y in range(24)]

    for r in run_intcode_program(program, 0, 0):
        if len(IO_queue) == 3:
            instruction_queue.append(
                (IO_queue[0], IO_queue[1], IO_queue[2]))
            IO_queue.clear()

    count = 0
    for i in range(len(instruction_queue)):
        x = instruction_queue[i][0]
        y = instruction_queue[i][1]
        if instruction_queue[i][2] == 2:
            count += 1
        tile = tiles[instruction_queue[i][2]]
        board[y][x] = tile

    print_board(board)
    print(count)
# Your puzzle answer was 462
