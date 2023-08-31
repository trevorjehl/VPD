#!/usr/bin/env python3
"""
Creates custom wafer-scanning G-code using gCodeClass.py

Copyright (C) Trevor Jehl, Stanford Nanofabrication Facility

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Created Jul 2023
by Trevor Jehl
tjehl@stanford.edu
Stanford Nanofabrication Facility 2023
"""

import numpy as np
import sys, os

# Allow imports from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from gCodeClass import *


def changeDefaultParams(classInstance):
    """ "
    If you would like to change any of the defualt parameters,
    you may do so by uncommenting and changing these lines. Otherwise,
    they will remain as defuault and configured for the Ender 3.
    """
    ###########################################
    # ALL VALUES IN MM UNLESS OTHERWISE NOTED #
    ###########################################

    ### ENDER 3 CONSTRAINTS ###
    # marlinPrinter.X_MAX = 220
    # marlinPrinter.Y_MAX = 220
    # marlinPrinter.Z_MAX = 250
    ###########################

    # PROCESS VALUES (in mm unless otherwuise noted)
    VPDScanner.TRAVEL_FEEDRATE = 2000  # Standard is 3000
    VPDScanner.SCANNING_MOVE_FEEDRATE = 90  # Adjust as needed to maintain hold of drop
    VPDScanner.EXTRUSION_MOTOR_FEEDRATE = 10

    VPDScanner.SCAN_HEIGHT = 1.5
    # VPDScanner.TRAVEL_HEIGHT = 40 # Make sure this is well above the highest point (cuevette lid)
    VPDScanner.DROPLET_DIAMETER = 39  # mm

    VPDScanner.CUEVETTE_X = 190.5
    VPDScanner.CUEVETTE_Y = 47.5
    VPDScanner.CUEVETTE_Z = 4

    # Wafer specific global vars (in mm unless otherwuise noted)
    VPDScanner.WAFER_DIAM = 100  # 4in wafer
    VPDScanner.EDGE_GAP = 10  # How far in from the wafer edge to scan

    # VPDScanner.RACK_TEETH_PER_CM = 3.183
    # VPDScanner.GEAR_TEETH = 16
    VPDScanner.RACK_TEETH_PER_CM = 6.36619
    VPDScanner.GEAR_TEETH = 30

    VPDScanner.SYRINGE_CAPACITY = 1.0
    VPDScanner.SYRINGE_LENGTH = 58.0


def main(filename):
    """
    Initializes, calls, and executes G-Code commands.
    """
    scanner = VPDScanner(filename, sample_volume=0.05)
    changeDefaultParams(scanner)

    start_volume = 0.05
    end_volume = 0.15
    increment = 0.02

    num_cycles = (end_volume - start_volume) // increment + 1
    print(f"The loop will run {num_cycles} cycles.")

    all_commands = []

    scanner.startGCode()
    all_commands.append(scanner.commands)
    for volume in np.arange(start_volume, end_volume, increment):
        scanner = VPDScanner(filename, volume)

        scanner.loadSyringe()
        scanner.doWaferScan()
        scanner.unloadSyringe()

        all_commands.append(scanner.commands)

    scanner_final = VPDScanner(filename, volume)

    scanner_final.endGCode()
    scanner_final.writeToFile()

    all_commands.append(scanner_final.commands)

    if ".gcode" not in filename:
        filename += ".gcode"

    with open(filename, "w") as file:
        for list in all_commands:
            for command in list:
                file.write(f"{command}\n")


if __name__ == "__main__":
    """
    This is executed when run from the command line.
    Parses command line args.
    """
    args = sys.argv[1:]

    filename = args[0]

    main(filename)
