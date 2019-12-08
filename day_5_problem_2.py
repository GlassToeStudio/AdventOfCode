''' --- Part Two ---
The air conditioner comes online! Its cold air feels good for a while, but
then the TEST alarms start to go off. Since the air conditioner can't vent its
heat anywhere but back into the spacecraft, it's actually making the air
inside the ship warmer.

Instead, you'll need to use the TEST to extend the thermal radiators.
Fortunately, the diagnostic program (your puzzle input) is already equipped
for this. Unfortunately, your Intcode computer is not.

Your computer is only missing a few opcodes:

--  Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the
    instruction pointer to the value from the second parameter. Otherwise, it
    does nothing.
--  Opcode 6 is jump-if-false: if the first parameter is zero, it sets the
    instruction pointer to the value from the second parameter. Otherwise, it
    does nothing.
--  Opcode 7 is less than: if the first parameter is less than the second
    parameter, it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.
--  Opcode 8 is equals: if the first parameter is equal to the second
    parameter, it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.

Like all instructions, these instructions need to support parameter modes as
described above.

Normally, after an instruction is finished, the instruction pointer increases
by the number of values in that instruction. However, if the instruction
modifies the instruction pointer, that value is used and the instruction
pointer is not automatically increased.

For example, here are several programs that take one input, compare it to the
value 8, and then produce one output:

--  3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input
    is equal to 8; output 1 (if it is) or 0 (if it is not).
--  3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input
    is less than 8; output 1 (if it is) or 0 (if it is not).
--  3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input
    is equal to 8; output 1 (if it is) or 0 (if it is not).
--  3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input
    is less than 8; output 1 (if it is) or 0 (if it is not).

Here are some jump tests that take an input, then output 0 if the input was
zero or 1 if the input was non-zero:

--  3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
--  3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)

Here's a larger example:

3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99

The above example program uses an input instruction to ask for a single number.
The program will then output 999 if the input value is below 8, output 1000 if
the input value is equal to 8, or output 1001 if the input value is greater
than 8.

This time, when the TEST diagnostic program runs its input instruction to get
the ID of the system to test, provide it 5, the ID for the ship's thermal
radiator controller. This diagnostic test suite only outputs one number, the
diagnostic code.

What is the diagnostic code for system ID 5?
'''

import math

intcode = [
    3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 9, 90, 224, 1001, 224, -99, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 6, 224, 1, 223, 224, 223, 1102, 26, 62, 225, 1101, 11, 75, 225, 1101, 90, 43, 225, 2, 70, 35, 224, 101, -1716, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 4, 224, 224, 1, 223, 224, 223, 1101, 94, 66, 225, 1102, 65, 89, 225, 101, 53, 144, 224, 101, -134, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 5, 224, 1, 224, 223, 223, 1102, 16, 32, 224, 101, -512, 224, 224, 4, 224, 102, 8, 223, 223, 101, 5, 224, 224, 1, 224, 223, 223, 1001, 43, 57, 224, 101, -147, 224, 224, 4, 224, 102, 8, 223, 223, 101, 4, 224, 224, 1, 223, 224, 223, 1101, 36, 81, 225, 1002, 39, 9, 224, 1001, 224, -99, 224, 4, 224, 1002, 223, 8, 223, 101, 2, 224, 224, 1, 223, 224, 223, 1, 213, 218, 224, 1001, 224, -98, 224, 4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 224, 223, 223, 102, 21, 74, 224, 101, -1869, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 7, 224, 1, 224, 223, 223, 1101, 25, 15, 225, 1101, 64, 73, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 1008, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 329, 1001, 223, 1, 223, 1007, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 344, 101, 1, 223, 223, 108, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 359, 101, 1, 223, 223, 108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 374, 1001, 223, 1, 223, 7, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 389, 1001, 223, 1, 223, 8, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 404, 1001, 223, 1, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 419, 101, 1, 223, 223, 1008, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 434, 101, 1, 223, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 449, 1001, 223, 1, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 464, 101, 1, 223, 223, 107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 479, 1001, 223, 1, 223, 8, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 494, 1001, 223, 1, 223, 1108, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 509, 101, 1, 223, 223, 1107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 524, 101, 1, 223, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 539, 101, 1, 223, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 554, 101, 1, 223, 223, 1107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 569, 1001, 223, 1, 223, 8, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 584, 101, 1, 223, 223, 1108, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 599, 101, 1, 223, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 614, 101, 1, 223, 223, 1007, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 629, 1001, 223, 1, 223, 7, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 644, 101, 1, 223, 223, 1007, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 659, 1001, 223, 1, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 674, 101, 1, 223, 223, 4, 223, 99, 226]


# intcode = [3,9,8,9,10,9,4,9,99,-1,8]


class Instruction:
    def __init__(self, fn, parameters):
        self.__num_parameters__ = parameters
        self.steps = parameters + 1 if parameters > 0 else math.inf
        self.fn = fn

    def get_params(self, address, intcodes):
        start = address + 1
        end = start + self.__num_parameters__
        p = intcodes[start:end]
        # print(f"4 Params = {p}")
        return p

    def update_steps(self, steps):
        self.steps = steps

    def execute(self, modes, params, intcodes, address):
        self.fn(modes, params, intcodes, address)


# intcode program methods
def format_opcode(opcode):
    sopcode = str(opcode)
    length = len(sopcode)
    for i in range(length, 5):
        sopcode = f"{0}{sopcode}"
    return sopcode


def read_full_opcode(opcode):
    opcode = int(opcode[-2:])
    return opcode


def get_modes(opcode):
    return opcode[0:3]


def get_param_by_mode(mode, val, codes):
    return codes[val] if mode == '0' else val


# Operations:
def add_operation(modes, params, codes, address):
    ''' Adds the values found at the two intcode positions

        Args:
            index_1 (int): Rhe location of the first opcode.
            index_2 (int): The location of the second opcode.
            codes (int[]): The array of opcodes.

        Returns:
            int: The sum of the values found at the given locations
            in the codes array.
    '''

    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)
    codes[params[2]] = param_1 + param_2


def mul_operation(modes, params, codes, address):
    ''' Multiplies the values found at the two intcode positions

    Args:
        index_1 (int): Rhe location of the first opcode.
        index_2 (int): The location of the second opcode.
        codes (int[]): The array of opcodes.

    Returns:
        int: The product of the values found at the given locations
        in the codes array.
    '''

    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)
    codes[params[2]] = param_1 * param_2


def input_operation(modes, params, codes, address):
    user_input = int(input("\t -- Please input a variable: "))
    codes[params[0]] = user_input


def output_operation(modes, params, codes, address):
    print(f"\t -- The value at position {params[0]} is {codes[params[0]]}")


def jump_if_true_operation(modes, params, codes, address):
    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)

    if param_1 != 0:
        instructions[5].update_steps(param_2 - address)
    else:
        instructions[5].update_steps(len(params) + 1)


def jump_if_false_operation(modes, params, codes, address):
    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)

    if param_1 == 0:
        instructions[6].update_steps(param_2 - address)
    else:
        instructions[6].update_steps(len(params) + 1)


def less_than_operation(modes, params, codes, address):
    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)
    if param_1 < param_2:
        codes[params[2]] = 1
    else:
        codes[params[2]] = 0


def equals_operation(modes, params, codes, address):
    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)
    if param_1 == param_2:
        codes[params[2]] = 1
    else:
        codes[params[2]] = 0


def halt_operation(modes, params, codes, address):
    print("\nEnding program\n\n")


# Setup
add_instruction = Instruction(add_operation, 3)
mult_instruction = Instruction(mul_operation, 3)
input_instruction = Instruction(input_operation, 1)
output_instruction = Instruction(output_operation, 1)
jump_if_true_instruction = Instruction(jump_if_true_operation, 2)
jump_if_false_instruction = Instruction(jump_if_false_operation, 2)
less_than_instruction = Instruction(less_than_operation, 3)
equals_instruction = Instruction(equals_operation, 3)
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
    99: halt_instruction
    }


# Main
def run_intcode_program(intcode):
    ''' Run the intcode program ;)

    Args:
        intcode (int[]): the intcode program
    '''

    address = 0
    step = 0
    length = len(intcode)

    print("Starting program...\n")
    while (address < length):
        full_opcode = format_opcode(intcode[address])
        opcode = read_full_opcode(full_opcode)
        modes = get_modes(full_opcode)
        params = instructions[opcode].get_params(address, intcode)
        instructions[opcode].execute(modes, params, intcode, address)
        address += instructions[opcode].steps


if __name__ == "__main__":
    run_intcode_program(intcode)
    # Your puzzle answer was: 3176266
