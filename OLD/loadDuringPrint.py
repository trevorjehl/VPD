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
    VPDScanner.TRAVEL_FEEDRATE = 1000  # Standard is 3000
    VPDScanner.SCANNING_MOVE_FEEDRATE = (
        1000  # Adjust as needed to maintain hold of drop
    )
    VPDScanner.EXTRUSION_MOTOR_FEEDRATE = 5

    # VPDScanner.TIP_HEIGHT = 3
    VPDScanner.TRAVEL_HEIGHT = (
        34  # Make sure this is well above the highest point (cuevette lid)
    )
    VPDScanner.DROPLET_SIZE = 25  # mm

    VPDScanner.CUEVETTE_X = 190.5
    VPDScanner.CUEVETTE_Y = 47.5
    VPDScanner.CUEVETTE_Z = 4

    # Wafer specific global vars (in mm unless otherwuise noted)
    # VPDScanner.WAFER_DIAM = 101.6 # 4in wafer
    # VPDScanner.EDGE_GAP = 5 # How far in from the wafer edge to scan

    # VPDScanner.RACK_TEETH_PER_CM = 3.183
    # VPDScanner.GEAR_TEETH = 16
    VPDScanner.RACK_TEETH_PER_CM = 6.36619
    VPDScanner.GEAR_TEETH = 30

    # VPDScanner.SYRINGE_CAPACITY = 3.0
    # VPDScanner.SYRINGE_LENGTH = 41.0


def main(filename):
    """ Main entry point of the app """
    scanner = VPDScanner(filename, sample_volume=0.500)
    changeDefaultParams(scanner)

    scanner.startGCode()
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
