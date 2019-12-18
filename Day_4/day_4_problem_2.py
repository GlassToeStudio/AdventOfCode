''' --- Part Two ---
An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

--  112233 meets these criteria because the digits never decrease and all
    repeateddigits are exactly two digits long.
--  123444 no longer meets the criteria (the repeated 44 is part of a larger
    group of 444).
--  111122 meets the criteria (even though 1 is repeated more than twice, it
    still contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?
'''


def check_increasing(num):
    ''' Return true if each consecutive digit is greater than or equal to
    the previous degit (left to right), false otherwise.
    '''

    num = str(num)
    for i in range(5):
        if num[i] <= num[i + 1]:
            continue
        else:
            return False

    return True


def check_two_consecutive(num):
    ''' Return true if num contains a set of exactly two repeating digits,
    false otherwise.
    '''

    num = f"_{num}_"
    for i in range(1, 6):
        if (num[i] == num[i + 1]
                and num[i + 1] != num[i + 2]
                and num[i] != num[i - 1]):
            return True

    return False


if __name__ == "__main__":
    passwords = 0
    for i in range(236491, 713787 + 1):
        if check_increasing(i) is True and check_two_consecutive(i) is True:
            passwords += 1

    print(
        "The total number of possible passwords" +
        f" in the given range are {passwords}"
        )
    # Your puzzle answer was 757.
