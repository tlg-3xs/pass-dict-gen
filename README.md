# pass-dict-gen
Custom password dictionary generator written in python
Creates password dictionaries from a list of words and/or phrases.
At the moment, it's features are:
- Replaces some letters with it's numeric equivalent.
- Replaces s and S with dollars.
- Replaces a and A with @.
- Makes combinations with provided and/or actual year.
- Makes combinations with punctuation symbols.

ToDo:
- Make the code clearer.
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
This is a project for improve my own python knowledge, and is meant for auditing own passwords strength. I'm not responsible for improper use.
