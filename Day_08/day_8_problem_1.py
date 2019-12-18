''' --- Day 8: Space Image Format ---
The Elves' spirits are lifted when they realize you have an opportunity to
reboot one of their Mars rovers, and so they are curious if you would spend a
brief sojourn on Mars. You land your ship near the rover.

When you reach the rover, you discover that it's already in the process of
rebooting! It's just waiting for someone to enter a BIOS password. The Elf
responsible for the rover takes a picture of the password (your puzzle input)
and sends it to you via the Digital Sending Network.

Unfortunately, images sent via the Digital Sending Network aren't encoded with
any normal encoding; instead, they're encoded in a special Space Image Format.
None of the Elves seem to remember why this is the case. They send you the
instructions to decode it.

Images are sent as a series of digits that each represent the color of a
single pixel. The digits fill each row of the image left-to-right, then move
downward to the next row, filling rows top-to-bottom until every pixel of the
image is filled.

Each image actually consists of a series of identically-sized layers that are
filled in this way. So, the first digit corresponds to the top-left pixel of
the first layer, the second digit corresponds to the pixel to the right of
that on the same layer, and so on until the last digit, which corresponds to
the bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data
123456789012 corresponds to the following image layers:

    Layer 1: 123
             456

    Layer 2: 789
             012

The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would
like you to find the layer that contains the fewest 0 digits. On that layer,
what is the number of 1 digits multiplied by the number of 2 digits?
'''

import math
from collections import Counter


def process_data(image_data, width, height):
    processed_data = []
    start = 0
    length = width * height
    num_layers = int(len(image_data) / length)
    end = length
    for i in range(num_layers):
        processed_data.append([int(x) for x in image_data[start:end]])
        start = end
        end += length
    return processed_data


def find_least(arr, num):
    index = 0
    least = math.inf
    for i in range(len(arr)):
        c = count_occurences(arr[i], num)
        if c < least:
            index = i
            least = c
    return index


def count_occurences(arr, num):
    count = Counter(arr)
    return count[num]


def get_answer(arr, num):
    index = find_least(arr, num)
    ones = count_occurences(arr[index], 1)
    twos = count_occurences(arr[index], 2)
    return ones * twos


if __name__ == "__main__":
    width = 25
    height = 6
    # Just too much data to keep in this .py file :(
    with open("Day_08/Data/day-8.txt", "r") as in_file:
        input_data = in_file.read()
    layer_data = process_data(input_data, width, height)
    print(
        "\nThe number of 1s multiplied by the nuumber of 2s"
        f" on the layer with the least 0s is : {get_answer(layer_data, 0)}\n")
# Your puzzle answer was 2016
