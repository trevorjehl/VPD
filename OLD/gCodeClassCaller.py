#!/usr/bin/env python3
"""
Creates custom wafer-scanning Gcode

Created Aug 2023
by Trevor Jehl
"""

from gCodeClass import *
import sys


def changeDefaultParams(classInstance):
    """"
    If you would like to change any of the defualt parameters,
    you may do so by uncommenting and changing these lines. Otherwise,
    they will remain as defuault and configured for the ender3.
    """
    ###########################################
    # ALL VALUES IN MM UNLESS OTHERWISE NOTED #
    ###########################################

    # ENDER 3 CONSTRAINTS
    # marlinPrinter.X_MAX = 220
    # marlinPrinter.Y_MAX = 220
    # marlinPrinter.Z_MAX = 250

    # PROCESS VALUES (in mm unless otherwuise noted)
    VPDScanner.TRAVEL_FEEDRATE = 2000  # Standard is 3000
    VPDScanner.SCANNING_MOVE_FEEDRATE = (
        1500  # Adjust as needed to maintain hold of drop
    )
    VPDScanner.EXTRUSION_MOTOR_FEEDRATE = 5

    # VPDScanner.TIP_HEIGHT = 3
    # VPDScanner.TRAVEL_HEIGHT = 40 # Make sure this is well above the highest point (cuevette lid)
    VPDScanner.DROPLET_SIZE = 2  # mm

    # VPDScanner.CUEVETTE_X = 200
    # VPDScanner.CUEVETTE_Y = 25
    # VPDScanner.CUEVETTE_Z = 10

    # Wafer specific global vars (in mm unless otherwuise noted)
    # VPDScanner.WAFER_DIAM = 101.6 # 4in wafer
    # VPDScanner.EDGE_GAP = 5 # How far in from the wafer edge to scan


def main(filename):
    """ Main entry point of the app """
    scanner = VPDScanner(filename, sample_volume=0.500)
    changeDefaultParams(scanner)

    scanner.startGCode()
    scanner.useCuevette(dispense=False)
    scanner.doWaferScan()
    scanner.useCuevette(dispense=True)

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
