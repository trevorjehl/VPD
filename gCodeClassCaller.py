#!/usr/bin/env python3
"""
Creates custom wafer-scanning Gcode

Created Aug 2023
by Trevor Jehl
"""

from gCodeClass import *
import sys

def main(filename):
    """ Main entry point of the app """
    scanner = VPDScanner(filename)
    print(scanner.getEFeedRate)

    scanner.startGCode()

    scanner.useCuevette(dispense = False)
    scanner.doWaferScan()
    scanner.useCuevette(dispense = True)

    
    scanner.endGCode()
    scanner.writeToFile()


if __name__ == "__main__":
    """
    This is executed when run from the command line.
    """
    commands = []
    args = sys.argv[1:]
    filename = args[0]
    main(filename)