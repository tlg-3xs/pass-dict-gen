# pass-dict-gen
Pass-Dict-Gen is a tool developed in Python, designed to generate custom password dictionaries derived from a user-provided list of words and/or phrases. The current functionality of this utility encompasses the following features:
- Substitution of certain letters with their numeric equivalents, enhancing the complexity of the resultant passwords.
- Replacement of the letters 's' and 'S' with the dollar symbol ('$'), further diversifying the password pool.
- Substitution of the letters 'a' and 'A' with the '@' symbol, adding an additional layer of complexity.
- Generation of password combinations incorporating the current year or a user-specified year, providing a temporal aspect to the password creation process.
- Creation of password combinations that include punctuation symbols, thereby increasing the potential password permutations.

Future Development:
I'm currently in the process of refining the codebase to enhance readability and maintainability, ensuring that Pass-Dict-Gen remains a robust and user-friendly tool for password dictionary generation.
```
usage: passgen.py [-h] [-i [INPUT]] [-o [OUTPUT]] [-y [YEAR]] [--all] [-d]
                  [-at] [-l] [-min MIN] [-max MAX] [-q | -v]

Creates a custom password wordlist from a set of keywords and phrases.

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT], --input [INPUT]
                        Input file for keywords. If not specified defaults to
                        stdin.
  -o [OUTPUT], --output [OUTPUT]
                        Output file. If not specified defaults to stdout.
  -y [YEAR], --year [YEAR]
                        Year for making combinations. Can be specified
                        multiple times. If it's specified without value
                        defaults to actual year.
  --all                 Makes all posible combinations. -y value can be
                        specified normally (by default assumes -y).
  -d, --dollar          Replaces s and S with $.
  -at                   Replaces a and A with @.
  -l, --l337, --l33t    Replaces letters with numbers.
  -min MIN, --minimum MIN
                        Minimum length of password. Default=1
  -max MAX, --maximum MAX
                        Maximum length of password. Default=200
  -q, --quiet           Suppresses informative output.
  -v, --verbose         Adds more informative output.
```
## Disclaimer
This project is designed for the purpose of enhancing my personal understanding of Python and is intended to be used for auditing the strength of one's own passwords. It is not designed or intended to be used for any illegal activities, including unauthorized access to systems or data. The creator of this project does not condone such misuse and will not be held responsible for any damages or legal consequences resulting from such activities. Users are advised to use this tool responsibly and in compliance with all applicable laws and regulations.
