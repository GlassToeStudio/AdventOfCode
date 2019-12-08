''' --- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a
password. The Elves had written the password on a sticky note, but someone
threw it out.

However, they do remember a few key facts about the password:

--  It is a six-digit number.
--  The value is within the range given in your puzzle input.
--  Two adjacent digits are the same (like 22 in 122345).
--  Going from left to right, the digits never decrease; they only ever
    increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

--  111111 meets these criteria (double 11, never decreases).
--  223450 does not meet these criteria (decreasing pair of digits 50).
--  123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?

Your puzzle input is 236491-713787.
'''


def check_increasing(num):
    ''' Return true if each consecutive digit is greater than or equal to
    the previous digit (left to right), false otherwise.
    '''

    num = str(num)
    for i in range(5):
        if num[i] <= num[i + 1]:
            continue
        else:
            return False

    return True


def check_consecutive(num):
    ''' Return true if at least two consecutive digits are equal,
    false otherwise.
    '''

    num = str(num)
    for i in range(5):
        if num[i] == num[i + 1]:
            return True

    return False


if __name__ == "__main__":
    passwords = 0
    for i in range(236491, 713787 + 1):
        if check_increasing(i) is True and check_consecutive(i) is True:
            passwords += 1

    print(
        "The total number of possible passwords" +
        f" in the given range are {passwords}"
        )
    # Your puzzle answer was 1169.
