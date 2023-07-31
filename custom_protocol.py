#!/usr/bin/env python3
"""
Creates custom wafer-scanning Gcode

Created Jul 2023
by Trevor Jehl
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from custom_commands import *

def main():
    """ Main entry point of the app """
    args = sys.argv[1:]
    filename = args[0]
    


if __name__ == "__main__":
    """
    This is executed when run from the command line.
    """
    main()