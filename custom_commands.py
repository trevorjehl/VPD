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


def startGCode(lst):
    lst.append("G21 ; set units to millimeters")
    lst.append("M82 ;absolute extrusion mode")
    lst.append("M302 S0; always allow extrusion (disable checking)")
    lst.append("G92 E0 ; Reset Extruder")
    lst.append("G28 ; Home all axes")
    lst.append("G90; Absolute positioning")
    lst.append("G92 E0 X0 Y0 Z0; Set home position")
    #Set extruder feedrate
    lst.append(f"G1 F{E_FEEDRATE} E0")
    #Set XYZ feedrate, move up
    lst.append("G1 Z2.0 F{E_FEEDRATE} ; Move up to prevent scrating")

    return lst


def centerHead(lst):
    nonExtrudeMove(lst, Z=3)
    nonExtrudeMove(lst, X=(X_MAX/2), Y=(Y_MAX)/2)
    nonExtrudeMove(nonExtrudeMove(lst, Z=0.2))

    return lst


def endGCode(lst):
    lst.append("G91 ;Relative positioning")
    lst.append("G1 Z10 ; Raise Z")
    lst.append("G90 ;Absolute positioning")
    lst.append(f"G1 X0 Y{Y_MAX} ;Present print")

    return lst


def write_to_gcode(lst, filename):
    """
    At the end of usage, write all commands to a G-code file
    in the local directory of filename "filename."
    """
    # "w" indicates write the new file, "+" Plus sign indicates
    # both read and write for Python create file operation.
    f= open(filename + ".gcode","w+")
    for command in lst:
        f.write(command + "\n")
    
    # Close the file, writing the lines.
    f.close()