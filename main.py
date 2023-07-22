import random

from PIL import Image
import sys


def ascii_to_binary(ascii_char) -> str:
    foo = ord(ascii_char)
    return bin(foo)[2:].zfill(9)


def encode(_message: str, _img: Image, contrast: int = 0) -> Image:
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
    unencoded_msg = ""
    for pixel in list(_img.getdata()):
        ascii_buffer = ""
        for value in pixel:
            _value = bin(value)[2:].zfill(9)
            ascii_buffer += _value[-3:]
        unencoded_msg += chr(int(ascii_buffer, 2))
    return unencoded_msg


if __name__ == '__main__':
    arguments = sys.argv

    assert arguments.count("-E") >= 1 and arguments.count("-D") < 1 or arguments.count("-D") >= 1 and arguments.count("-E") < 1, "Only one of the parameters -E or -D must be given to indicate if encoding or decoding."
    assert arguments.count("-m") == 1 if arguments.count("-E") >= 1 else arguments.count("-m") == 0, 'Expected argument -m was not given when trying to encode' if arguments.count("-m") == 0 and arguments.count("-E") == 1 else "Problems with -m"
    assert arguments.count("-i") == 1, 'Expected argument -i was not given' if arguments.count("-i") == 0 else "Only one parameter -m is expected"
    assert arguments.count("-n") <= 1, "Only one parameter -n is expected"

    if arguments.count("-m") >= 1:
        message = arguments[arguments.index("-m") + 1]
    image = Image.open(arguments[arguments.index("-i") + 1])
    if arguments.count("-E") == 1:
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
