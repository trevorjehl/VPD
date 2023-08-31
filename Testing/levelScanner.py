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

    # VPDScanner.SCAN_HEIGHT = 3.0
    # VPDScanner.TRAVEL_HEIGHT = 40 # Make sure this is well above the highest point (cuevette lid)
    # VPDScanner.DROPLET_DIAMETER = 40  # mm

    # Wafer specific global vars (in mm unless otherwuise noted)
    VPDScanner.WAFER_DIAM = 100  # 4in wafer
    VPDScanner.EDGE_GAP = 4  # How far in from the wafer edge to scan

    # VPDScanner.RACK_TEETH_PER_CM = 3.183
    # VPDScanner.GEAR_TEETH = 16
    VPDScanner.RACK_TEETH_PER_CM = 6.36619
    VPDScanner.GEAR_TEETH = 30

    VPDScanner.SYRINGE_CAPACITY = 1.0
    VPDScanner.SYRINGE_LENGTH = 58.0


def main(filename):
    """
    Go to the four corners of the 4in wafer. Beep
    and wait at each corner, waiting for user input. After
    the first cycle, go to each corner again. Then unload
    syringe and reset the printer.
    """
    scanner = VPDScanner(filename, sample_volume=0.00)
    changeDefaultParams(scanner)

    scanner.startGCode()

    scanner.loadSyringe()

    scanner.centerHead()
    scanner.nonExtrudeMove({"Z": 0, "F": 500})

    max_radius = (VPDScanner.WAFER_DIAM / 2) - VPDScanner.EDGE_GAP

    X_component = max_radius * math.cos(math.radians(45))
    Y_component = max_radius * math.sin(math.radians(45))

    # Do the whole thing twice
    for i in range(2):
        for x_dir in [1, -1]:
            for y_dir in [1, -1]:
                scanner.relativePos()
                # Using commands.append avoids the head offset
                scanner.commands.append(
                    f"G0 X{ x_dir * X_component:.4f} Y{ y_dir * Y_component:.4f} F500 "
                )

                scanner.beep()
                scanner.waitForUserInput()

                scanner.absPos()
                scanner.centerHead()

    scanner.unloadSyringe()

    scanner.endGCode()
    scanner.writeToFile()


if __name__ == "__main__":
    """
    This is executed when run from the command line.
    Parses command line args.
    """
    args = sys.argv[1:]

    filename = args[0]

    main(filename)
