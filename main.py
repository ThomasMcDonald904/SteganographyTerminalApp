import math
import random

from PIL import Image
import sys

proper_character_offset = 32


def convert_rgba_to_rgb(rgba_image):
    # Create a new RGB image with a white background
    rgb_image = Image.new("RGB", rgba_image.size, "white")

    # Paste the RGBA image onto the RGB image, removing the alpha channel
    rgb_image.paste(rgba_image, mask=rgba_image.split()[3])

    return rgb_image


def ascii_to_binary(ascii_char) -> str:
    foo = ord(ascii_char)
    return bin(foo)[2:].zfill(9)


def encode(_message: str, _img: Image, contrast: int = 0) -> Image:
    # Encoding header pixels. 511 is the max size of information stored in one pixel
    # The number of header pixels and the size of the message is encoded as specific unicode characters to facilitate
    # implementation. In order to get single characters, 32 is added to reach proper characters Ex: 'ȟ' is 511 and '!' is 1

    # Image mustn't have transparency because the subtle changes of encoding are more obvious
    if _img.mode in ('RGBA', 'LA') or (_img.mode == 'P' and 'transparency' in _img.info):
        _img = convert_rgba_to_rgb(_img)

    nbr_size_header_pixels = math.ceil(len(_message) / 511)

    header_length_character = chr(nbr_size_header_pixels + proper_character_offset)
    header_characters = [header_length_character]
    # Header pixel computation
    for i in range(nbr_size_header_pixels - 1):
        header_characters.append(chr(511 + proper_character_offset))
    header_characters.append(chr(len(_message) % 511 + proper_character_offset))

    # Prepending header pixels to message
    _message = "".join(header_characters) + _message
    pixels = list(_img.getdata())
    encoded_pixels = []
    for index, char in enumerate(_message):
        char_binary = ascii_to_binary(char)
        packages = [char_binary[i:i + 3] for i in range(0, len(char_binary), 3)]
        encoded_pixel = []
        for i in range(3):
            encoded_pixel.append(int(bin(pixels[index][i])[2:][:-3] + packages[i], 2) + contrast)
        encoded_pixels.append(tuple(encoded_pixel))
    _img.putdata(encoded_pixels)
    return _img


def decode(_img: Image) -> str:
    img_data = _img.getdata()

    unencoded_msg = ""
    for pixel in list(img_data):
        ascii_buffer = ""
        for value in pixel:
            _value = bin(value)[2:].zfill(9)
            ascii_buffer += _value[-3:]
        unencoded_msg += chr(int(ascii_buffer, 2))
    # Get and process header data
    header_length = ord(unencoded_msg[0]) - proper_character_offset
    message_length = 0
    for character_index in range(header_length):
        message_length += ord(unencoded_msg[character_index + 1]) - proper_character_offset
    return unencoded_msg[header_length + 1:message_length + header_length + 1]


if __name__ == '__main__':
    arguments = sys.argv

    assert arguments.count("-E") >= 1 and arguments.count("-D") < 1 or arguments.count("-D") >= 1 and arguments.count(
        "-E") < 1, "Only one of the parameters -E or -D must be given to indicate if encoding or decoding."
    assert arguments.count("-m") == 1 if arguments.count("-E") >= 1 else arguments.count(
        "-m") == 0, 'Expected argument -m was not given when trying to encode' if arguments.count(
        "-m") == 0 and arguments.count("-E") == 1 else "Problems with -m"
    assert arguments.count("-i") == 1, 'Expected argument -i was not given' if arguments.count(
        "-i") == 0 else "Only one parameter -m is expected"
    assert arguments.count("-n") <= 1, "Only one parameter -n is expected"

    if arguments.count("-m") >= 1:
        message = arguments[arguments.index("-m") + 1]
    image = Image.open(arguments[arguments.index("-i") + 1])

    if arguments.count("-E") == 1:
        check_nbr_header_pixels = math.ceil(len(message) / 511) + 1
        nbr_pixels = image.width * image.height
        assert nbr_pixels >= check_nbr_header_pixels + len(
            message), f"Message is too large for image, message is worth {len(message)}px, given image is {nbr_pixels}px - {check_nbr_header_pixels} header px"

        if arguments.count("-C"):
            img = encode(message, image, 50)
        else:
            img = encode(message, image)
        if arguments.count("-n") == 1:
            img.save(arguments[arguments.index("-n") + 1] + ".png")
        else:
            img.save(str(random.randint(11111111, 99999999)) + ".png")
    elif arguments.count("-D") == 1:
        print(decode(image))
