''' --- Part Two ---
Now that your FFT is working, you can decode the real signal.

The real signal is your puzzle input repeated 10000 times. Treat this new
signal as a single input list. Patterns are still calculated as before, and
100 phases of FFT are still applied.

The first seven digits of your initial input signal also represent the message
offset. The message offset is the location of the eight-digit message in the
final output list. Specifically, the message offset indicates the number of
digits to skip before reading the eight-digit message. For example, if the
first seven digits of your initial input signal were 1234567, the eight-digit
message would be the eight digits after skipping 1,234,567 digits of the final
output list. Or, if the message offset were 7 and your final output list were
98765432109876543210, the eight-digit message would be 21098765. (Of course,
your real message offset will be a seven-digit number, not a one-digit number
like 7.)

Here is the eight-digit message in the final output list after 100 phases. The
message offset given in each input has been highlighted. (Note that the inputs
given below are repeated 10000 times to find the actual starting input lists.)

--  03036732577212944063491565474664 becomes 84462026.
--  02935109699940807407585447034323 becomes 78725270.
--  03081770884921959731165446850517 becomes 53553731.

After repeating your input signal 10000 times and running 100 phases of FFT,
what is the eight-digit message embedded in the final output list?
'''


def format_input(in_file):
    return [int(x) for x in in_file]


def run_FFT(sequence, phases):
    for phase in range(0, phases):
        sum = 0
        for i in range(len(sequence) - 1, -1, -1):
            sum += sequence[i]
            sequence[i] = sum % 10
    return sequence


def format_output(data):
    s = ''
    for x in data:
        s += f'{x}'
    return int(s)


if __name__ == "__main__":
    with open("Day_16/Data/day-16.txt", "r") as in_file:
        sequence = format_input(in_file.read())

    phases = 100
    scaler = 10_000
    offset = format_output(sequence[:7])
    repeated_length = len(sequence) * scaler
    useful_length = repeated_length - offset
    useful_scaler = useful_length // len(sequence) + 1
    sequence = sequence * useful_scaler
    sequence = sequence[-useful_length:]
    result = run_FFT(sequence, phases)
    final = format_output(result[:8])
    print(f'The eight digits the starting at the {offset}\'th '
          f'position in the final output list are {final}.')
# Your puzzle answer was 48776785
