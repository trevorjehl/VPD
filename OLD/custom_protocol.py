#!/usr/bin/env python3
"""
Creates custom wafer-scanning Gcode

Created Jul 2023
by Trevor Jehl
"""

from custom_commands import *
import sys


def main(filename):
    """ Main entry point of the app """

    startGCode(commands)
    doWaferScan(commands)

    endGCode(commands)

    write_to_gcode(commands, filename)


if __name__ == "__main__":
    """
    This is executed when run from the command line.
    """
    commands = []
    args = sys.argv[1:]
    filename = args[0]
    main(filename)
