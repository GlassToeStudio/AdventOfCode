''' --- Day 7: Amplification Circuit ---
Based on the navigational maps, you're going to need to send more power to
your ship's thrusters to reach Santa in time. To do this, you'll need to
configure a series of amplifiers already installed on the ship.

There are five amplifiers connected in series; each one receives an input
signal and produces an output signal. They are connected such that the first
amplifier's output leads to the second amplifier's input, the second
amplifier's output leads to the third amplifier's input, and so on. The first
amplifier's input value is 0, and the last amplifier's output leads to your
ship's thrusters.

    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O

The Elves have sent you some Amplifier Controller Software (your puzzle input),
a program that should run on your existing Intcode computer. Each amplifier
will need to run a copy of the program.

When a copy of the program starts running on an amplifier, it will first use
an input instruction to ask the amplifier for its current phase setting (an
integer from 0 to 4). Each phase setting is used exactly once, but the Elves
can't remember which amplifier needs which phase setting.

The program will then call another input instruction to get the amplifier's
input signal, compute the correct output signal, and supply it back to the
amplifier with an output instruction. (If the amplifier has not yet received
an input signal, it waits until one arrives.)

Your job is to find the largest output signal that can be sent to the
thrusters by trying every possible combination of phase settings on the
amplifiers. Make sure that memory is not shared or reused between copies of
the program.

For example, suppose you want to try the phase setting sequence 3,1,2,4,0,
which would mean setting amplifier A to phase setting 3, amplifier B to
setting 1, C to 2, D to 4, and E to 0. Then, you could determine the output
signal that gets sent from amplifier E to the thrusters with the following
steps:

--  Start the copy of the amplifier controller software that will run on
    amplifier A. At its first input instruction, provide it the amplifier's
    phase setting, 3. At its second input instruction, provide it the input
    signal, 0. After some calculations, it will use an output instruction to
    indicate the amplifier's output signal.
--  Start the software for amplifier B. Provide it the phase setting (1) and
    then whatever output signal was produced from amplifier A. It will then
    produce a new output signal destined for amplifier C.
--  Start the software for amplifier C, provide the phase setting (2) and
    the value from amplifier B, then collect its output signal.
--  Run amplifier D's software, provide the phase setting (4) and input value,
    and collect its output signal.
--  Run amplifier E's software, provide the phase setting (0) and input value,
    and collect its output signal.

The final output signal from amplifier E would be sent to the thrusters.
However, this phase setting sequence may not have been the best one; another
sequence might have sent a higher signal to the thrusters.

Here are some example programs:

--  Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

    3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
    Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

    3,23,3,24,1002,24,10,24,1002,23,-1,23,
    101,5,23,23,1,24,23,23,4,23,99,0,0

--  Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

    3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
    1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0

Try every combination of phase settings on the amplifiers. What is the highest
signal that can be sent to the thrusters?
'''

import math
from itertools import permutations as permu


class Instruction:
    def __init__(self, operation_fn, num_params):
        self.__num_parameters__ = num_params
        self.operation_fn = operation_fn
        self.update_steps(num_params + 1 if num_params > 0 else math.inf)

    def get_params(self, address, intcodes):
        start = address + 1
        end = start + self.__num_parameters__
        p = intcodes[start:end]
        return p

    def update_steps(self, steps):
        self.steps = steps

    def execute(self, modes, params, intcodes, address):
        self.r = self.operation_fn(modes, params, intcodes, address)
        return self.r


intcode = [
    3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 46, 67, 76, 101, 118, 199, 280, 361, 442, 99999, 3, 9, 1002, 9, 4, 9, 1001, 9, 2, 9, 102, 3, 9, 9, 101, 3, 9, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 3, 9, 102, 2, 9, 9, 1001, 9, 2, 9, 1002, 9, 3, 9, 4, 9, 99, 3, 9, 101, 3, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 2, 9, 1002, 9, 5, 9, 101, 5, 9, 9, 1002, 9, 4, 9, 101, 5, 9, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 1001, 9, 5, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99]

index_map = [0]
amp_output = [0]
user_input = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# intcode program methods
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


# Helper
def get_param_by_mode(mode, val, codes):
    return codes[val] if mode == '0' else val


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


def generate_sequences():
    ''' Return all permutations of the given range of numbers.

    Returns:
        int[[]]: Every permutation of the given range.
    '''

    sequence = []
    for i, j, k, l, m in permu(range(5), 5):
        sequence.append([i, j, k, l, m])
    return sequence


# Operations:
def add_operation(modes, params, codes, address):
    ''' Adds together numbers read from two positions, params[1] and params[1]
        and stores the result in a third position, params[2].

    Args:
        modes (int[]): The parameter modes for the instruction.
        params (int[]): The parameters for the instruction.
        codes (int[]): The intcode program
    '''

    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)
    codes[params[2]] = param_1 + param_2


def mul_operation(modes, params, codes, address):
    ''' Multiplies together numbers read from two positions, params[1] and
    params[1] and stores the result in a third position, params[2].

    Args:
        modes (int[]): The parameter modes for the instruction.
        params (int[]): The parameters for the instruction.
        codes (int[]): The intcode program
    '''

    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)
    codes[params[2]] = param_1 * param_2


def input_operation(modes, params, codes, address):
    codes[params[0]] = user_input[index_map[0]]
    if index_map[0] < len(user_input) - 1:
        index_map[0] = index_map[0] + 1


def output_operation(modes, params, codes, address):
    # print(f"\t -- The value at position {params[0]} is {codes[params[0]]}")
    amp_output[0] = codes[params[0]]


def jump_if_true_operation(modes, params, codes, address):
    ''' If the first parameter params[0] is non-zero, it sets the instruction
    pointer to the value from the second parameter params[1]. Otherwise,
    it does nothing.

    Args:
        modes (int[]): The parameter modes for the instruction.
        params (int[]): The parameters for the instruction.
        codes (int[]): The intcode program
    '''

    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)

    if param_1 != 0:
        instructions[5].update_steps(param_2 - address)
    else:
        instructions[5].update_steps(len(params) + 1)


def jump_if_false_operation(modes, params, codes, address):
    ''' If the first parameter param[0] is zero, it sets the instruction
    pointer to the value from the second parameter params[1].
    Otherwise, it does nothing.

    Args:
        modes (int[]): The parameter modes for the instruction.
        params (int[]): The parameters for the instruction.
        codes (int[]): The intcode program
    '''

    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)

    if param_1 == 0:
        instructions[6].update_steps(param_2 - address)
    else:
        instructions[6].update_steps(len(params) + 1)


def less_than_operation(modes, params, codes, address):
    ''' If the first parameter params[0] is less than the second
    parameter params[1], it stores 1 in the position given by the third
    parameter params[2]. Otherwise, it stores 0.

    Args:
        modes (int[]): The parameter modes for the instruction.
        params (int[]): The parameters for the instruction.
        codes (int[]): The intcode program
    '''

    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)

    if param_1 < param_2:
        codes[params[2]] = 1
    else:
        codes[params[2]] = 0


def equals_operation(modes, params, codes, address):
    ''' If the first parameter params[0] is equal to the second
    parameter params[1], it stores 1 in the position given by the third
    parameter params[2]. Otherwise, it stores 0. 0.

    Args:
        modes (int[]): The parameter modes for the instruction.
        params (int[]): The parameters for the instruction.
        codes (int[]): The intcode program
    '''

    param_1 = get_param_by_mode(modes[2], params[0], codes)
    param_2 = get_param_by_mode(modes[1], params[1], codes)

    if param_1 == param_2:
        codes[params[2]] = 1
    else:
        codes[params[2]] = 0


def halt_operation(modes, params, codes, address):
    ''' Halts the program.

    Returns:
        int: opcode instruction 99
    '''
    return 99


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

    result = 0
    address = 0

    while (address < len(intcode)):
        full_opcode = format_opcode(intcode[address])
        opcode = read_full_opcode(full_opcode)
        modes = get_modes(full_opcode)
        params = instructions[opcode].get_params(address, intcode)
        instructions[opcode].execute(modes, params, intcode, address)
        address += instructions[opcode].steps


def run_automated_program(highest_signal, num_amps):
    # For every permutation of phase setting sequences
    sequence = generate_sequences()

    for i in range(len(sequence)):
        index_map[0] = 0
        amp_output[0] = 0

        user_input[0] = sequence[i][0]
        user_input[1] = 0
        user_input[2] = sequence[i][1]
        user_input[4] = sequence[i][2]
        user_input[6] = sequence[i][3]
        user_input[8] = sequence[i][4]

        # For a total of 5 amplifiers
        for n in range(num_amps):
            run_intcode_program(get_copy_of_program(intcode))
            if index_map[0] % 2 == 0:
                user_input[index_map[0] + 1] = amp_output[0]

        if amp_output[0] > highest_signal:
            highest_signal = amp_output[0]

    return highest_signal


if __name__ == "__main__":
    highest_signal = 0
    highest_signal = run_automated_program(highest_signal, 5)

    print(
        "The highest signal that can " +
        f"be sent to the thrusters is {highest_signal}"
    )
# Your puzzle answer was 87138
