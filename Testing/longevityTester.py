
#!/usr/bin/env python3
"""
Take N lines and repeat them n times, counting the number of repeats in the gcode
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import sys


def main(filename, repeats):
    """ Main entry point of the app """

    if ".gcode" not in filename:
        filename += ".gcode"

    ogCommandsList = []
    with open(filename, 'r') as file:
        ogLines = file.readlines()
        print(ogLines)
        for line in ogLines:
            ogCommandsList.append(line.strip())

    with open(filename, 'w') as file:
        for repetition in range(repeats):
            for ogCommand in ogCommandsList:
                # print(ogCommand)
                file.write(ogCommand + '\n')
            file.write(f'; {repetition + 1} repeat \n')


if __name__ == "__main__":
    """ This is executed when run from the command line """

    args = sys.argv[1:]

    filename = args[0]
    repeats = int(args[1])
    main(filename, repeats)