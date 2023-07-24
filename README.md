# SteganographyTerminalApp

## Usage
Run ``main.py`` using python 3.6+ <br>
Refrain from using characters after **U+01DF** if ``-T`` isn't enabled, because the encoding algorythm cannot support hex past **0x01DF**

If encoding an image with the message: "The quick brown dog jumped over the lazy fox."<br>
```
$ python .\main.py -e -i path\to\image.png -m "The quick brown dog jumped over the lazy fox."
```
## Flags

### Mandatory when encoding
- ``-e`` tells that you're encoding
- ``-i`` Path to image
- ``-m`` Message (must be in quotes)
### Optional when encoding
  - ``-C`` Adds contrast to encoded pixels 
    - Destroys message, only for debugging
  - ``-N`` Output file name 
    - If omitted, a random 8-digit number while be given
  - ``-T`` **To-Do** Uses or adds a transparency layer to be able to encode larger unicode characters
    - After encoding, a modified transparency layer can be more obvious
    - If not enabling, refrain from using characters after **U+01DF**
### Mandatory when decoding
- ``-d`` tells that you're decoding
- ``-i`` Path to image