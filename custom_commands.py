#!/usr/bin/env python3
"""
This file is designed to list out a set of custom 
G-Code commands for use in wafer scanning with a 
3D printer.

Created Jul 2023
by Trevor Jehl
"""

__author__ = "Trevor Jehl"
__version__ = "0.1.0"
# __license__ = "MIT"

import os
from pygcode import *
from nativeGCodeCommands import *

# Create a list of all commands
COMMANDS = []

#ENDER 3 CONSTRAINTS
X_MAX = 220
Y_MAX = 220
Z_MAX = 250

# PROCESS VALUES (in mm unless otherwuise noted)
EDGE_LENGTH = 5
XYZ_FEEDRATE = 1125 # Standard is 1125
E_FEEDRATE = 2700 # Adjust as needed


# Wafer specific global vars (in mm unless otherwuise noted)
WAFER_DIAM = 101.6 # 4in wafer


def startGCode():
    COMMANDS.append("G21 ; set units to millimeters")
    COMMANDS.append("M82 ;absolute extrusion mode")
    COMMANDS.append("G92 E0 ; Reset Extruder")
    COMMANDS.append("G28 ; Home all axes")
    COMMANDS.append("G90; Absolute positioning")
    COMMANDS.append("G92 E0 X0 Y0 Z0; Set home position")
    #Set extruder feedrate
    COMMANDS.append(f"G1 F{E_FEEDRATE} E0")
    #Set XYZ feedrate, move up
    COMMANDS.append("G1 Z2.0 F{E_FEEDRATE} ; Move up to prevent scrating")


def centerHead():
    nonExtrudeMove(COMMANDS, Z=3)
    nonExtrudeMove(COMMANDS, X=(X_MAX/2), Y= (Y_MAX)/2)
    nonExtrudeMove(nonExtrudeMove(COMMANDS, Z=0.2))


def write_to_gcode(filename):
    """
    At the end of usage, write all commands to a G-code file
    in the local directory of filename "filename."
    """
    # "w" indicates write the new file, "+" Plus sign indicates
    # both read and write for Python create file operation.
    f= open(filename + ".gcode","w+")
    for command in COMMANDS:
        f.write(command + "\n")
    
    # Close the file, writing the lines.
    f.close()

# def main():
#     """ Main entry point of the app """


# if __name__ == "__main__":
#     """ This is executed when run from the command line """
#     main()