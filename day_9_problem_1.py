''' --- Day 9: Sensor Boost ---
You've just said goodbye to the rebooted rover and left Mars when you receive
a faint distress signal coming from the asteroid belt. It must be the Ceres
monitoring station!

In order to lock on to the signal, you'll need to boost your sensors. The
Elves send up the latest BOOST program - Basic Operation Of System Test.

While BOOST (your puzzle input) is capable of boosting your sensors, for
tenuous safety reasons, it refuses to do so until the computer it runs on
passes some checks to demonstrate it is a complete Intcode computer.

Your existing Intcode computer is missing one key feature: it needs support
for parameters in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in
position mode: the parameter is interpreted as a position. Like position mode,
parameters in relative mode can be read from or written to.

The important difference is that relative mode parameters don't count from
address 0. Instead, they count from a value called the relative base. The
relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current
relative base. When the relative base is 0, relative mode parameters and
position mode parameters with the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7
refers to memory address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

--  Opcode 9 adjusts the relative base by the value of its only parameter. The
    relative base increases (or decreases, if the value is negative) by the
    value of the parameter. For example, if the relative base is 2000, then
    after the instruction 109,19, the relative base would be 2019. If the next
    instruction were 204,-34, then the value at address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

--  The computer's available memory should be much larger than the initial
    program. Memory beyond the initial program starts with the value 0 and can
    be read or written like any other memory. (It is invalid to try to access
    memory at a negative address, though.)
--  The computer should have support for large numbers. Some instructions near
    the beginning of the BOOST program will verify this capability.

Here are some example programs that use these features:

--  109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input
    and produces a copy of itself as output.
--  1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
--  104,1125899906842624,99 should output the large number in the middle.

The BOOST program will ask for a single input; run it in test mode by
providing it the value 1. It will perform a series of checks on each opcode,
output any opcodes (and the associated parameter modes) that seem to be
functioning incorrectly, and finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should
report no malfunctioning opcodes when run in test mode; it should only output
a single value, the BOOST keycode. What BOOST keycode does it produce?
'''

import math
from itertools import permutations as permu


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


def generate_sequences(start, end):
    ''' Return all permutations of the given range of numbers.

    Args:
        start (int): Beginning of the range.
        end (int): End of the range.

    Returns:
        int[[]]: Every permutation of the given range.
    '''
    sequence = []
    for i, j, k, l, m in permu(range(start, end), 5):
        sequence.append([i, j, k, l, m])
    return sequence


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
    codes[param_1] = input_queue.pop()
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


def automated_output_operation(codes, params, **kwargs):
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

    input_queue.append(codes[params[0]])
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
input_instruction = Instruction(automated_input_operation, 1)
output_instruction = Instruction(output_operation, 1)
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

intcode = [
    1102, 34463338, 34463338, 63,
    1007, 63, 34463338, 63,
    1005, 63, 53,
    1102, 1, 3, 1000,
    109, 988,
    209, 12,
    9, 1000,
    209, 6,
    209, 3,
    203, 0,
    1008, 1000, 1, 63,
    1005, 63, 65,
    1008, 1000, 2, 63,
    1005, 63, 904,
    1008, 1000, 0, 63,
    1005, 63, 58,
    4, 25,
    104, 0,
    99,
    4, 0,
    104, 0,
    99,
    4, 17,
    104, 0,
    99,
    0,0,1102,1,21,1004,1101,28,0,1016,1101,0,27,1010,1102,36,1,1008,1102,33,1,1013,1101,0,22,1012,1101,0,37,1011,1102,34,1,1017,1102,466,1,1027,1102,1,484,1029,1102,1,699,1024,1102,1,1,1021,1101,0,0,1020,1102,1,24,1015,1101,0,473,1026,1101,653,0,1022,1102,26,1,1007,1102,25,1,1006,1101,0,39,1014,1102,646,1,1023,1101,690,0,1025,1102,1,29,1019,1101,32,0,1018,1101,30,0,1002,1101,0,20,1001,1102,1,38,1005,1102,1,23,1003,1101,0,31,1000,1101,35,0,1009,1101,0,493,1028,109,5,1208,0,37,63,1005,63,201,1001,64,1,64,1106,0,203,4,187,1002,64,2,64,109,-4,2107,36,8,63,1005,63,223,1001,64,1,64,1105,1,225,4,209,1002,64,2,64,109,18,21107,40,41,-9,1005,1010,243,4,231,1105,1,247,1001,64,1,64,1002,64,2,64,109,6,21107,41,40,-9,1005,1016,267,1001,64,1,64,1106,0,269,4,253,1002,64,2,64,109,-19,21102,42,1,5,1008,1011,42,63,1005,63,291,4,275,1105,1,295,1001,64,1,64,1002,64,2,64,109,15,1205,0,309,4,301,1105,1,313,1001,64,1,64,1002,64,2,64,109,-27,2101,0,9,63,1008,63,20,63,1005,63,333,1106,0,339,4,319,1001,64,1,64,1002,64,2,64,109,19,21102,43,1,6,1008,1019,45,63,1005,63,363,1001,64,1,64,1105,1,365,4,345,1002,64,2,64,109,1,21108,44,47,-3,1005,1011,385,1001,64,1,64,1106,0,387,4,371,1002,64,2,64,109,-22,1201,9,0,63,1008,63,21,63,1005,63,411,1001,64,1,64,1106,0,413,4,393,1002,64,2,64,109,9,1207,0,19,63,1005,63,433,1001,64,1,64,1106,0,435,4,419,1002,64,2,64,109,-9,2107,30,8,63,1005,63,453,4,441,1105,1,457,1001,64,1,64,1002,64,2,64,109,25,2106,0,10,1001,64,1,64,1106,0,475,4,463,1002,64,2,64,109,11,2106,0,0,4,481,1001,64,1,64,1105,1,493,1002,64,2,64,109,-18,2108,21,-6,63,1005,63,511,4,499,1106,0,515,1001,64,1,64,1002,64,2,64,109,-12,2108,18,6,63,1005,63,535,1001,64,1,64,1106,0,537,4,521,1002,64,2,64,109,19,21101,45,0,-7,1008,1010,45,63,1005,63,563,4,543,1001,64,1,64,1105,1,563,1002,64,2,64,109,-10,1207,-5,31,63,1005,63,581,4,569,1106,0,585,1001,64,1,64,1002,64,2,64,109,-8,2102,1,5,63,1008,63,21,63,1005,63,611,4,591,1001,64,1,64,1105,1,611,1002,64,2,64,109,5,1201,0,0,63,1008,63,21,63,1005,63,633,4,617,1106,0,637,1001,64,1,64,1002,64,2,64,109,13,2105,1,6,1001,64,1,64,1106,0,655,4,643,1002,64,2,64,109,-7,1202,-3,1,63,1008,63,26,63,1005,63,681,4,661,1001,64,1,64,1106,0,681,1002,64,2,64,109,12,2105,1,2,4,687,1001,64,1,64,1105,1,699,1002,64,2,64,109,-28,1208,8,30,63,1005,63,717,4,705,1106,0,721,1001,64,1,64,1002,64,2,64,109,10,1202,1,1,63,1008,63,40,63,1005,63,745,1001,64,1,64,1105,1,747,4,727,1002,64,2,64,109,10,21108,46,46,-2,1005,1012,765,4,753,1105,1,769,1001,64,1,64,1002,64,2,64,109,-2,1205,8,781,1106,0,787,4,775,1001,64,1,64,1002,64,2,64,109,-9,2101,0,0,63,1008,63,23,63,1005,63,809,4,793,1105,1,813,1001,64,1,64,1002,64,2,64,109,9,1206,8,831,4,819,1001,64,1,64,1106,0,831,1002,64,2,64,109,-9,2102,1,-2,63,1008,63,22,63,1005,63,855,1001,64,1,64,1106,0,857,4,837,1002,64,2,64,109,4,21101,47,0,10,1008,1017,50,63,1005,63,877,1105,1,883,4,863,1001,64,1,64,1002,64,2,64,109,18,1206,-4,895,1105,1,901,4,889,1001,64,1,64,4,64,99,21101,0,27,1,21102,915,1,0,1106,0,922,21201,1,56639,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,1,942,0,1106,0,922,22102,1,1,-1,21201,-2,-3,1,21101,0,957,0,1106,0,922,22201,1,-1,-2,1106,0,968,22102,1,-2,-2,109,-3,2106,0,0]

addresses = [0, 0, 0, 0, 0]
input_queue = []
relative_base = [0]


def load_program(intcode):
    program = {}
    for i in range(len(intcode)):
        program[i] = intcode[i]
    return program


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
    return r


if __name__ == "__main__":
    input_queue.append(1)
    run_intcode_program(load_program(intcode), 0, 0)
    # Your puzzle answer was 4261108180

