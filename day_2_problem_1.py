''' --- Day 2: 1202 Program Alarm ---
On the way to your gravity assist around the Moon, your ship computer beeps
angrily about a "1202 program alarm". On the radio, an Elf is already
explaining how to handle the situation: "Don't worry, that's perfectly norma--"
The ship computer bursts into flames.

You notify the Elves that the computer's magic smoke seems to have escaped.
"That computer ran Intcode programs like the gravity assist program it was
working on; surely there are enough spare parts up there to build a new
Intcode computer!"

An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
To run one, start by looking at the first integer (called position 0).
Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what
to do; for example, 99 means that the program is finished and should
immediately halt. Encountering an unknown opcode means something went wrong.

Opcode 1 adds together numbers read from two positions and stores the result
in a third position. The three integers immediately after the opcode tell you
these three positions - the first two indicate the positions from which you
should read the input values, and the third indicates the position at which
the output should be stored.

For example, if your Intcode computer encounters 1,10,20,30, it should read
the values at positions 10 and 20, add those values, and then overwrite the
value at position 30 with their sum.

Opcode 2 works exactly like opcode 1, except it multiplies the two inputs
instead of adding them. Again, the three integers after the opcode indicate
where the inputs and outputs are, not their values.

Once you're done processing an opcode, move to the next one by stepping
forward 4 positions.

For example, suppose you have the following program:

1,9,10,3,2,3,11,0,99,30,40,50
For the purposes of illustration, here is the same program split into multiple
lines:

1,9,10,3,
2,3,11,0,
99,
30,40,50

The first four integers, 1,9,10,3, are at positions 0, 1, 2, and 3. Together,
they represent the first opcode (1, addition), the positions of the two inputs
(9 and 10), and the position of the output (3). To handle this opcode, you
first need to get the values at the input positions: position 9 contains 30,
and position 10 contains 40. Add these numbers together to get 70. Then, store
this value at the output position; here, the output position (3) is at
position 3, so it overwrites itself. Afterward, the program looks like this:

1,9,10,*70*,
2,3,11,0,
99,
30,40,50

Step forward 4 positions to reach the next opcode, 2. This opcode works just
like the previous, but it multiplies instead of adding. The inputs are at
positions 3 and 11; these positions contain 70 and 50 respectively.
Multiplying these produces 3500; this is stored at position 0:

*3500*,9,10,70,
2,3,11,0,
99,
30,40,50

Stepping forward 4 more positions arrives at opcode 99, halting the program.

    - 1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
    - 2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
    - 2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
    - 1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.

Once you have a working computer, the first step is to restore the gravity
assist program (your puzzle input) to the "1202 program alarm" state it had
just before the last computer caught fire. To do this, before running the
program, replace position 1 with the value 12 and replace position 2 with the
value 2. What value is left at position 0 after the program halts?

'''

intcode = [
    1, 0, 0, 3,
    1, 1, 2, 3,
    1, 3, 4, 3,
    1, 5, 0, 3,
    2, 1, 10, 19,
    1, 19, 5, 23,
    1, 6, 23, 27,
    1, 27, 5, 31,
    2, 31, 10, 35,
    2, 35, 6, 39,
    1, 39, 5, 43,
    2, 43, 9, 47,
    1, 47, 6, 51,
    1, 13, 51, 55,
    2, 9, 55, 59,
    1, 59, 13, 63,
    1, 6, 63, 67,
    2, 67, 10, 71,
    1, 9, 71, 75,
    2, 75, 6, 79,
    1, 79, 5, 83,
    1, 83, 5, 87,
    2, 9, 87, 91,
    2, 9, 91, 95,
    1, 95, 10, 99,
    1, 9, 99, 103,
    2, 103, 6, 107,
    2, 9, 107, 111,
    1, 111, 5, 115,
    2, 6, 115, 119,
    1, 5, 119, 123,
    1, 123, 2, 127,
    1, 127, 9, 0,
    99,  # Program should halt here.
    2, 0, 14, 0
]


def add_intcodes(index_1, index_2, codes):
    ''' Adds the values found at the two intcode positions

        Args:
            index_1 (int): Rhe location of the first opcode.
            index_2 (int): The location of the second opcode.
            codes (int[]): The array of opcodes.

        Returns:
            int: The sum of the values found at the given locations
            in the codes array.
    '''

    return codes[index_1] + codes[index_2]


def mul_intcodes(index_1, index_2, codes):
    ''' Multiplies the values found at the two intcode positions

    Args:
        index_1 (int): Rhe location of the first opcode.
        index_2 (int): The location of the second opcode.
        codes (int[]): The array of opcodes.

    Returns:
        int: The product of the values found at the given locations
        in the codes array.
    '''

    return codes[index_1] * codes[index_2]


def run_intcode_program(pos_1, pos_2, intcode):
    ''' Calculate the resultant value at position 0 by changing the values
    at pos_1 and pos_2 and running the program.

    Args:
        pos_1 (int): value for position 1
        pos_2 (int): value for position 2
        intcode (int[]): the intcode program

    Returns:
        int: value at position 0
    '''

    # Per the instructions, alter the intcode at positions 1 and 2.
    intcode[1] = pos_1
    intcode[2] = pos_2

    address = 0
    step = 4
    add_operator = 1
    mul_operator = 2
    halt_operator = 99
    length = len(intcode)

    while (address < length):
        opcode = intcode[address]
        param_1 = intcode[address + 1]
        param_2 = intcode[address + 2]
        param_3 = intcode[address + 3]

        # Opcode == 99, program halt.
        if opcode == halt_operator:
            address = length

        # Opcode == 1, add the values at the 2nd and 3rd position,
        # and place that value into the 4th position.
        elif opcode == add_operator:
            intcode[param_3] = add_intcodes(param_1, param_2, intcode)
            address += step

        # Opcode == 2, multiply the values at the 2nd and 3rd position,
        # and place that value into the 4th position.
        elif opcode == mul_operator:
            intcode[param_3] = mul_intcodes(param_1, param_2, intcode)
            address += step

    return intcode[0]


print(f"Final intcode at position 0: {run_intcode_program(12, 2, intcode)}")
# Your puzzle answer was: 3267740
