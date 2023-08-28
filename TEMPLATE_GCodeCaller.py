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

from gCodeClass import *
import sys


def changeDefaultParams(classInstance):
    """"
    If you would like to change any of the defualt parameters,
    you may do so by uncommenting and changing these lines. Otherwise,
    they will remain as defuault and configured for the Ender 3.
    """
    ###########################################
    # ALL VALUES IN MM UNLESS OTHERWISE NOTED #
    ###########################################

    #### ENDER 3 CONSTRAINTS ####
    # marlinPrinter.X_OFFSET = -8
    # marlinPrinter.Y_OFFSET = 11
    # marlinPrinter.Z_OFFSET = 0

    # marlinPrinter.X_MAX = 235
    # marlinPrinter.Y_MAX = 235
    # marlinPrinter.Z_MAX = 250
    #############################

    # MOTOR SPEEDS
    VPDScanner.TRAVEL_FEEDRATE = 2000  # Controls travel movement speed
    # Controls scanning speed. Adjust as needed to maintain hold of drop
    VPDScanner.SCANNING_MOVE_FEEDRATE = 100
    VPDScanner.EXTRUSION_MOTOR_FEEDRATE = 10

    # Vertical offset (from the z endstop) to scan the drop at
    VPDScanner.SCAN_HEIGHT = 2.6
    # Make sure this is well above the highest point (cuevette lid)
    VPDScanner.TRAVEL_HEIGHT = 40

    # CUEVETTE INFO (XYZ location of the cuevette)
    VPDScanner.CUEVETTE_X = 190.5
    VPDScanner.CUEVETTE_Y = 47.5
    VPDScanner.CUEVETTE_Z = 4

    # WAFER VARIABLES
    VPDScanner.WAFER_DIAM = 100.0  # 100mm = 4in wafer
    VPDScanner.EDGE_GAP = 10  # How far in from the wafer edge to scan
    VPDScanner.DROPLET_DIAMETER = 4  # mm

    # SCAN HEAD VARIABLES
    # Do not change the syringe variables unless a different syringe is being used.
    VPDScanner.SYRINGE_CAPACITY = 1.0
    VPDScanner.SYRINGE_LENGTH = 58.0
    # Do not change the following variables unless the physical gears have been changed.
    VPDScanner.RACK_TEETH_PER_CM = 6.36619
    VPDScanner.GEAR_TEETH = 30


def main(filename):
    """ 
    Initializes, calls, and executes G-Code commands.
    """
    scanner = VPDScanner(filename, sample_volume=0.05)
    changeDefaultParams(scanner)

    scanner.startGCode()

    # scanner.useCuevette(dispense = False)

    scanner.loadSyringe()
    scanner.doWaferScan()

    # scanner.useCuevette(dispense = True)
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
