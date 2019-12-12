''' --- Part Two ---
It's no good - in this configuration, the amplifiers can't generate a large
enough output signal to produce the thrust you'll need. The Elves quickly talk
you through rewiring the amplifiers into a feedback loop:

      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)

Most of the amplifiers are connected as they were before; amplifier A's output
is connected to amplifier B's input, and so on. However, the output from
amplifier E is now connected into amplifier A's input. This creates the
feedback loop: the signal will be sent through the amplifiers many times.

In feedback loop mode, the amplifiers need totally different phase settings:
integers from 5 to 9, again each used exactly once. These settings will cause
the Amplifier Controller Software to repeatedly take input and produce output
many times before halting. Provide each amplifier its phase setting at its
first input instruction; all further input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this
process. Each one should continue receiving and sending signals until it halts.

All signals sent or received in this process will be between pairs of
amplifiers except the very first signal and the very last signal. To start the
process, a 0 signal is sent to amplifier A's input exactly once.

Eventually, the software on the amplifiers will halt after they have processed
the final loop. When this happens, the last output signal from amplifier E is
sent to the thrusters. Your job is to find the largest output signal that can
be sent to the thrusters using the new phase settings and feedback loop
arrangement.

Here are some example programs:

--  Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

    3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5

--  Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

    3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10

Try every combination of the new phase settings on the amplifier feedback
loop. What is the highest signal that can be sent to the thrusters?
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
        start = address + 1
        end = start + self.__num_parameters__
        p = intcodes[start:end]
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
def get_param_by_mode(modes, params, codes):
    ''' Return the values of the given parameters based on their position mode.

    Notes:
        0, position mode, which causes the parameter to be interpreted as a
        position - if the parameter is 50, its value is the value stored
        at address 50 in memory.

        1, immediate mode. In immediate mode, a parameter is interpreted
        as a value - if the parameter is 50, its value is simply 50.

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction

    Returns:
        tuple<int>: param_1, param_2
    '''

    param_1 = codes[params[0]] if modes[2] == '0' else params[0]
    param_2 = codes[params[1]] if modes[1] == '0' else params[1]
    return param_1, param_2


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
    ''' Adds together numbers read from two positions, params[1] and params[1]
        and stores the result in a third position, params[2].

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction.

    Returns:
        int: opcode instruction 1
    '''

    param_1, param_2 = get_param_by_mode(modes, params, codes)
    codes[params[2]] = param_1 + param_2
    return 1


def mul_operation(codes, params, modes, **kwargs):
    ''' Multiplies together numbers read from two positions, params[1] and
    params[1] and stores the result in a third position, params[2].

    Args:
        codes (int[]): The intcode program
        params (int[]): The parameters for the instruction.
        modes (int[]): The parameter modes for the instruction.

    Returns:
        int: opcode instruction 2
    '''

    param_1, param_2 = get_param_by_mode(modes, params, codes)
    codes[params[2]] = param_1 * param_2
    return 2


def input_operation(codes, params, **kwargs):
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
        int: opcode instruction 1
    '''

    user_input = int(input("\t -- Please input a variable: "))
    codes[params[0]] = user_input
    return 3


def automated_input_operation(codes, params, **kwargs):
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

    codes[params[0]] = input_queue.pop()
    return 3


def output_operation(codes, params, **kwargs):
    ''' Print to the console, teh output of the given instruction.

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

    print(f"\t -- The value at position {params[0]} is {codes[params[0]]}")


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

    param_1, param_2 = get_param_by_mode(modes, params, codes)
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

    param_1, param_2 = get_param_by_mode(modes, params, codes)
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

    param_1, param_2 = get_param_by_mode(modes, params, codes)
    if param_1 < param_2:
        codes[params[2]] = 1
    else:
        codes[params[2]] = 0
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

    param_1, param_2 = get_param_by_mode(modes, params, codes)
    if param_1 == param_2:
        codes[params[2]] = 1
    else:
        codes[params[2]] = 0
    return 8


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
output_instruction = Instruction(automated_output_operation, 1)
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

intcode = [
    3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 46, 67, 76, 101, 118, 199, 280, 361, 442, 99999, 3, 9, 1002, 9, 4, 9, 1001, 9, 2, 9, 102, 3, 9, 9, 101, 3, 9, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 3, 9, 102, 2, 9, 9, 1001, 9, 2, 9, 1002, 9, 3, 9, 4, 9, 99, 3, 9, 101, 3, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 2, 9, 1002, 9, 5, 9, 101, 5, 9, 9, 1002, 9, 4, 9, 101, 5, 9, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 1001, 9, 5, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99]
addresses = [0, 0, 0, 0, 0]
input_queue = []


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
        if r == 4:
            addresses[current_amp] = current_address
            return r
        if r == 99:
            return r
    return r


def run_automated_program(num_amps, highest_signal):
    # For every permutation of phase setting sequences
    sequences = generate_sequences(5, 10)
    for seq in range(len(sequences)):
        programs = [get_copy_of_program(intcode) for x in range(5)]
        input_queue.append(0)
        halted = False
        for address in range(len(addresses)):
            addresses[address] = 0
        initialize_amps = True
        # Loop until the final amp halts
        while not halted:
            # For a total of 5 amplifiers
            for amp in range(num_amps):
                if initialize_amps:
                    input_queue.append(sequences[seq][amp])
                result_code = run_intcode_program(
                    programs[amp],
                    addresses[amp],
                    amp)
                if result_code == 99:
                    highest_signal = max(highest_signal, input_queue[-1])
                    halted = True
            initialize_amps = False
    return highest_signal


if __name__ == "__main__":
    highest_signal = run_automated_program(5, 0)

    print(
        "The highest signal that can " +
        f"be sent to the thrusters is {highest_signal}"
    )
# Your puzzle answer was 17279674
