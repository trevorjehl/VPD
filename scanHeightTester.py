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
import numpy as np
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

    ### ENDER 3 CONSTRAINTS ###
    # marlinPrinter.X_MAX = 220
    # marlinPrinter.Y_MAX = 220
    # marlinPrinter.Z_MAX = 250
    ###########################

    # PROCESS VALUES (in mm unless otherwuise noted)
    VPDScanner.TRAVEL_FEEDRATE = 2000  # Standard is 3000
    VPDScanner.SCANNING_MOVE_FEEDRATE = 90  # Adjust as needed to maintain hold of drop
    VPDScanner.EXTRUSION_MOTOR_FEEDRATE = 10

    VPDScanner.SCAN_HEIGHT = 3.0
    # VPDScanner.TRAVEL_HEIGHT = 40 # Make sure this is well above the highest point (cuevette lid)
    VPDScanner.DROPLET_DIAMETER = 40  # mm

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


    start_height = 1.6
    end_height = 3.0
    increment = 0.2

    VPDScanner.SCAN_HEIGHT = start_height

    num_cycles = (end_height - start_height - 1) // increment + 1
    print(f"The loop will run {num_cycles} cycles.")

    scanner.startGCode()
    for height in np.arange(start_height, end_height + increment, increment):
        VPDScanner.SCAN_HEIGHT = height
        print(VPDScanner.SCAN_HEIGHT)

        scanner.loadSyringe()
        scanner.doWaferScan()
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
