''' --- Part Two ---
Now you're ready to decode the image. The image is rendered by stacking the
layers and aligning the pixels with the same positions in each layer. The
digits indicate the color of the corresponding pixel: 0 is black, 1 is white,
and 2 is transparent.

The layers are rendered with the first layer in front and the last layer in
back. So, if a given position has a transparent pixel in the first and second
layers, a black pixel in the third layer, and a white pixel in the fourth
layer, the final image would have a black pixel at that position.

For example, given an image 2 pixels wide and 2 pixels tall, the image data
0222112222120000 corresponds to the following image layers:

    Layer 1: 02
             22

    Layer 2: 11
             22

    Layer 3: 22
             12

    Layer 4: 00
             00

Then, the full image can be found by determining the top visible pixel in each
position:

--  The top-left pixel is black because the top layer is 0.
--  The top-right pixel is white because the top layer is 2 (transparent), but
    the second layer is 1.
--  The bottom-left pixel is white because the top two layers are 2, but the
    third layer is 1.
--  The bottom-right pixel is black because the only visible pixel in that
    position is 0 (from layer 4).

So, the final image looks like this:

  01
  10

What message is produced after decoding your image?
'''

from PIL import Image


def process_data(image_data, width, height):
    data = []
    start = 0
    length = width * height
    num_layers = int(len(image_data) / length)
    end = length
    for i in range(num_layers):
        data.append([int(x) for x in image_data[start:end]])
        start = end
        end += length
    return data


def create_pixel_map(layer_data):
    data_map = layer_data[0]
    for layer in layer_data:
        for i in range(0, len(layer)):
            if data_map[i] == 2:
                data_map[i] = layer[i]
    return data_map


def format_pixel_data(layer_data, width, height):
    formatted_data = create_pixel_map(layer_data)
    pixel_data = []
    start = 0
    end = width
    for i in range(height):
        pixel_data.append(formatted_data[start:end])
        start = end
        end += width
    return pixel_data


def create_answer_text(pixel_map, width, height):
    answer = ''
    for row in range(height):
        for col in range(width):
            if pixel_map[row][col] == 1:
                answer = f"{answer}█"
            else:
                answer = f"{answer} "
        answer = f"{answer}\n"
    with open("Day_8/day-8-password.txt", "w", encoding='utf-8') as pass_file:
        pass_file.write(answer)
    print(answer)


def create_answer_image(pixel_map, p, width, height):
    for col in range(width):
        for row in range(height):
            if pixel_map[row][col] == 1:
                p[col, row] = (255, 255, 255)
            elif pixel_map[row][col] == 0:
                p[col, row] = (0, 0, 0)
    return p


if __name__ == "__main__":
    width = 25
    height = 6

    # Just too much data to keep in this .py file :(
    with open("Day_8/Data/day-8.txt", "r") as in_file:
        image_data = in_file.read()
    layer_data = process_data(image_data, width, height)
    pixel_map = format_pixel_data(layer_data, width, height)
    img = Image.new('RGB', (width, height), color='white')
    pixels = img.load()
    pixels = create_answer_image(pixel_map, pixels, width, height)
    create_answer_text(pixel_map, width, height)
    img.save('Day_8/day-8-password.png')

# Your puzzle answer was
# █  █ ████  ██  ████ █  █
# █  █    █ █  █    █ █  █
# ████   █  █      █  █  █
# █  █  █   █     █   █  █
# █  █ █    █  █ █    █  █
# █  █ ████  ██  ████  ██
