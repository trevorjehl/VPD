#!/usr/bin/env python3
"""
gCodeClass.py creates G-Code and VPDScanner classes,
which use G-Code to produce the commands neccesary to scan
a silicon wafer with a droplet.
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

import math


class marlinPrinter:
    # Leave class variables at these default values here
    # If you wish to change them, change them in your caller script
    X_MAX = 235
    Y_MAX = 235
    Z_MAX = 250

    X_OFFSET = -8
    Y_OFFSET = 11
    Z_OFFSET = 0

    def __init__(self, filename):
        """
        Creates the internal command list, captures the gcode filename to write to.
        """
        self.filename = filename

        self.commands = []  # Create list of G-Code commands

    def sanitizeCoords(func):
        """
        Takes the coords dict (ex. {'X': 5, 'F': 40.1}), adjusts for the printhead
        offset, adds decimal places to all coordinates, and limits the decimal places
        allowed to 4.
        """

        def addDecimalPoint(self, coords):
            """
            GCode can have some funky issues if locations are 
            given without decimals (ie. G1 X1 instead of G1 X1.).
            This function checks for compatibility and fixes if/as needed.
            """

            result = {}

            for axis, value in coords.items():
                if isinstance(value, int):  # if argument is an integer
                    result[axis] = f"{value}.0"
                elif isinstance(value, float) or isinstance(
                    value, str
                ):  # if argument is a float or string
                    str_val = str(value)
                    if (
                        "." not in str_val
                    ):  # if float but doesn't have a decimal point (e.g., 5.0)
                        result[axis] = f"{value}.0"
                    else:  # if the number is already formatted correctly
                        result[axis] = str_val
                else:
                    raise Exception(
                        "Attempted to add decimal point to an incompatible data class."
                    )

            return result

        def adjsutForOffset(self, coords):
            """"
            Given a 'coords' dict (ex. {'X': 10.0, 'Y': 5.0}),
            adjust for the head/tip/nozzle offset.
            """
            if coords is None:
                return {"X": None, "Y": None, "Z": None}

            for axis, value in coords.items():
                if axis == "X":
                    coords["X"] = value + marlinPrinter.X_OFFSET
                if axis == "Y":
                    coords["Y"] = value + marlinPrinter.Y_OFFSET
                if axis == "Z":
                    coords["Z"] = value + marlinPrinter.Z_OFFSET

            return coords

        def limitDecimalPlaces(self, coords, places=4):
            """
            Limit the decimal places allowed in commands.
            >>> print = GCodeGenerator("test")
            >>> print.limitDecimalPlaces({"X": 5.00010})
            {'X': '5.0001'}
            >>> print.limitDecimalPlaces({"X": 5.00010, 'Y': 100.1, 'Z': '10.00000'})
            {'X': '5.0001', 'Y': '100.1000', 'Z': '10.0000'}
            >>> print.limitDecimalPlaces({"X": "5.00010"})
            {'X': '5.0001'}
            """
            for axis, value in coords.items():
                value = float(value)
                coords[axis] = f"{value:.4f}"
            return coords

        def wrapper(instance, *args, **kwargs):
            """
            Given coords dict, adjust for offset,
            add decimals, and return the coordinates
            as strings. Calls helper functions with
            these purposes.
            """
            # retrive anything called 'coords' from a function's input
            coords_arg = kwargs.get("coords", None)
            # get all the arguments passed into a function
            args_list = list(args)

            # If no 'coords' arg found, then
            if not coords_arg:
                # Iterate through each argument to check for a dictionary containing position related keys
                for i, arg in enumerate(args):
                    if isinstance(arg, dict) and any(
                        key in ["X", "Y", "Z", "E", "F"] for key in arg
                    ):
                        coords_arg = arg
                        # Remove the found coordinates dictionary from the arguments list
                        args = args[:i] + args[i + 1 :]  # Remove the coords from args
                        break  # stop looking

            if (
                not coords_arg
            ):  # Raise an error if 'coords' argument is still not found after the checks
                raise ValueError("coords argument not found!")

            coords_arg = adjsutForOffset(instance, coords_arg)
            coords_arg = addDecimalPoint(instance, coords_arg)
            coords_arg = limitDecimalPlaces(instance, coords_arg)

            args_list[
                i
            ] = coords_arg  # Insert the modified coords_arg back into its original position
            args_tuple = tuple(
                args_list
            )  # Convert list back to tuple (it is initially a tuple)

            return func(instance, *args_tuple, **kwargs)

        return wrapper

    def undoHeadOffset(self, coords):
        """
        Some functions need to use the true XY values instead
        of adjusting for the head offset to locate a physical
        point in space. Some examples include the doCircle function,
        which needs the center point to be constant in space, and also
        when using the cuevette holder.
        """
        for axis, value in coords.items():
            value = float(value)
            if axis == "X":
                fixedX = value - marlinPrinter.X_OFFSET
                coords["X"] = f"{fixedX:.4f}"
            if axis == "Y":
                fixedY = value - marlinPrinter.Y_OFFSET
                coords["Y"] = f"{fixedY:.4f}"

        return coords

    @sanitizeCoords
    def nonExtrudeMove(self, coords, comment=None):
        """
        Move the extruder without extruding. 
        """
        move = "G0"  # base command

        for axis, value in coords.items():
            if axis == "F" and "Z" in coords.items():
                # Decrease feedrate if changing Z.
                move += f" {axis}{value/1.6}"
            else:
                move += f" {axis}{value}"

        if "F" not in move and "Z" in move:
            move += f" F{VPDScanner.TRAVEL_FEEDRATE / 1.6}"
        elif "F" not in move:
            move += f" F{VPDScanner.TRAVEL_FEEDRATE}"

        if move != "G0":
            if comment:
                # Add comment as appropriate for G-code clarity
                move += f" ;{comment}"
            self.commands.append(move.strip())

    @sanitizeCoords
    def doCircle(self, coords, comment=None):
        """
        Moves the printehead in a complete circle around the point
        specified by the coords dictionary. The values in the dictionary
        are RELATIVE, not absolute.
        >>> doCircle([], {'X': 20, 'Y': 20})
        ['G2 I20.0000 J20.0000']
        """
        if len(coords) >= 3:
            raise Exception("Passed 3 or more coordinates to the doCircle funciton.")

        coords = self.undoHeadOffset(coords)
        move = "G2"
        for axis, value in coords.items():
            if axis == "X":
                move += f" I{value}"
            if axis == "Y":
                move += f" J{value}"

        if move != "G2":
            if comment:
                move += f" ; {comment}"
            self.commands.append(move.strip())

    @sanitizeCoords
    def doCCWArc(self, coords, center_offset, radius, theta_deg, comment=None):
        """
        Given coords dict(center of rotation), arc radius, an angle,
        rotate around the center point theta degrees.
        """
        move = "G3"
        x = float(coords["X"])
        y = float(coords["Y"])
        theta_rad = math.radians(theta_deg)

        # Calculate the end point of the arc
        end_x = (x + center_offset[0]) + radius * math.cos(theta_rad)
        end_y = (y + center_offset[1]) + radius * math.sin(theta_rad)

        if "E" in coords.keys():
            val = coords["E"]
            move += f" E{val}"
        move += f" I{center_offset[0]:.4f} J{center_offset[1]:.4f} X{end_x:.4f} Y{end_y:.4f}"

        if move != "G3":
            if comment:
                move += f" ; {comment}"
            self.commands.append(move.strip())

    @sanitizeCoords
    def extrudeMove(self, coords, comment=None):
        """
        Move any set of X,Y,Z,E axes. E axis is ALWAYS 
        absolute positioning. E units are in mL. Specify
        'F' in the coords dict to determine the feedrate.
        """
        # self.commands.append('M83; Set E to relative positioning')
        self.commands.append("M82; Set E to absolute positioning")

        coord_axes = coords.keys()
        move = "G1"

        for axis, value in coords.items():
            move += f" {axis}{value}"
        if "F" not in move:
            move += f" F{VPDScanner.TRAVEL_FEEDRATE}"

        if move != "G1":
            if comment:
                move += f" ; {comment}"
            self.commands.append(move.strip())

    @sanitizeCoords
    def setStepsPerUnit(self, coords):
        """
        Use M92 to set the steps-per-unit for one or more axes. 
        This setting affects how many steps will be done for each 
        unit of movement.
        """
        coord_axes = coords.keys()
        move = "M92"

        for axis, value in coords.items():
            move += f" {axis}{value}"

        if move != "M92":
            move += " ; Set steps per unit."
            self.commands.append(move.strip())

    def relativePos(self):
        self.commands.append("G91 ; Set all axes to relative")

    def absPos(self):
        self.commands.append("G90 ; Set all axes to absolute")

    def homeAxes(self):
        self.commands.append("G28 ; Home all axes")

    def wait(self, seconds=0.5):
        self.commands.append(f"G4 S{seconds:.4f}")

    def waitForUserInput(self):
        self.commands.append("M0 ; Stop and wait")

    def waitForMovesToComplete(self):
        self.commands.append("M400")

    def beep(self, sec=0.2):
        """
        Beep for 'sec' seconds.
        """
        self.waitForMovesToComplete()
        self.commands.append(f"M300 P{(sec*1000):.4f} ; Beep.")

    def writeToFile(self):
        """"
        To be called at the end of the routine. Writes all
        commands line by line to a .gcode file. Filename defined
        when creating class instance.
        """
        filename = self.filename
        if ".gcode" not in filename:
            filename += ".gcode"

        with open(filename, "w") as file:
            for command in self.commands:
                file.write(f"{command}\n")


#####################################################
#####################################################
############### BEGIN CUSTOM COMMANDS ###############
#####################################################
#####################################################


class VPDScanner(marlinPrinter):
    # PROCESS VALUES (in mm unless otherwuise noted)
    TRAVEL_FEEDRATE = 2000  # Standard is 3000
    SCANNING_MOVE_FEEDRATE = 100  # Adjust as needed
    EXTRUSION_MOTOR_FEEDRATE = 10

    SCAN_HEIGHT = 2.6  # How high from the z-stop should the tip be to scan?
    TRAVEL_HEIGHT = 40  # Make sure this is well above the cuevette lid height
    DROPLET_DIAMETER = 4  # mm

    CUEVETTE_X = 190.5
    CUEVETTE_Y = 47.5
    CUEVETTE_Z = 4

    # Wafer specific global vars (in mm unless otherwuise noted)
    WAFER_DIAM = 100.0  # 4in wafer
    EDGE_GAP = 10  # How far in from the wafer edge to scan

    # Only adjust the paramaters below if the physical gears are modified
    RACK_TEETH_PER_CM = 6.36619
    GEAR_TEETH = 30

    SYRINGE_CAPACITY = 1.0
    SYRINGE_LENGTH = 58.0

    def __init__(self, filename, sample_volume, **kwargs):
        """"
        Creates a VPD scanner class object, which is a child of the
        marlinPrinter class. Filename will write the
        gcode to that file. Sample_volume defines how much liquid 
        the system will use during the scan. Passes other kwargs to 
        marlinPrinter.
        """
        super().__init__(filename, **kwargs)
        self.sample_volume = sample_volume

    def calcEFeedRate(self):
        """
        Assuming the motor has 3200 steps/rev, 
        calculate the feed rate such that the command 
        'G0 E1.0' dispenses exactly 1ml of solution. In other
        words, the this function calculates the parameter such that
        '1' system unit is equal to 1mL in the syringe.
        """
        mL = VPDScanner.SYRINGE_CAPACITY
        mm = VPDScanner.SYRINGE_LENGTH

        stepsPerRotation = 3200
        stepsPerDeg = stepsPerRotation / 360

        gearTeeth = VPDScanner.GEAR_TEETH
        gearTeethPerDegree = gearTeeth / 360

        rackTeethPerCm = VPDScanner.RACK_TEETH_PER_CM

        mLPerMM = mL / mm
        mLPerRackTooth = (mLPerMM * 10) / rackTeethPerCm
        mLPerGearDegree = mLPerRackTooth * gearTeethPerDegree

        degreePerML = 1 / mLPerGearDegree

        stepsPerML = degreePerML * stepsPerDeg

        return stepsPerML

    def startGCode(self):
        """
        Housekeeping -- mainly homes and then moves up.
        """
        self.commands.append("; BEGIN START GCODE")
        self.commands.append("G21 ; set units to millimeters")
        self.commands.append("M82 ;absolute extrusion mode")
        self.commands.append(
            "M302 S0; always allow extrusion (disable temp/length checking)"
        )
        self.commands.append("G92 E0 ; Reset Extruder")

        self.homeAxes()
        self.absPos()
        self.commands.append("G92 E0 X0 Y0 Z0; Set home position")

        # Set appropriate e_steps
        e_steps = self.calcEFeedRate()
        self.setStepsPerUnit({"E": e_steps})
        self.commands.append(
            f"M203 E{self.EXTRUSION_MOTOR_FEEDRATE:.4f} ; Set max E feedrate"
        )

        self.nonExtrudeMove(
            {"Z": 2.0}, "Move up to prevent scratching."
        )  # Set XYZ feedrate, move up
        self.commands.append(";")
        self.commands.append("; END START GCODE")
        self.commands.append(";")

    def calcRelPos(self, coords, xPoint, yPoint):
        """
        Given a point in space (coords) and
        the current absolute position, calculate the
        XY vector to travel from the abs to the point.
        """
        x = float(coords["X"])
        y = float(coords["Y"])
        return (xPoint - x, yPoint - y)

    def collectSample(self, volume=None):
        """"
        Assume needle tip is in location where ready to 
        collect, collect the volume.
        """
        if not volume:
            volume = self.sample_volume

        self.extrudeMove(
            {"E": self.SYRINGE_CAPACITY, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE}
        )
        self.wait()
        self.extrudeMove({"E": 0, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE / 2})
        self.wait()
        self.extrudeMove(
            {"E": self.SYRINGE_CAPACITY, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE}
        )
        self.wait()

    def dispenseSample(self, volume=None):
        """"
        Assume needle tip is in location where ready to 
        dispense, dispense the volume.
        """
        if not volume:
            volume = self.sample_volume

        self.extrudeMove({"E": 0, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.wait()
        self.extrudeMove(
            {"E": volume / 2, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE / 2}
        )
        self.wait()
        self.extrudeMove({"E": 0, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE / 2})
        self.wait()

    def useCuevette(self, dispense: bool):
        """
        If dispense is true, will dispense sample. Otherwise 
        will collect sample.
        Using the cuevette measurements (found in
        global variables), move up, move over, move down,
        and deposit the scanned droplet.
        """
        # move up
        self.nonExtrudeMove({"Z": VPDScanner.TRAVEL_HEIGHT})
        # move over cuevette
        self.nonExtrudeMove(
            {
                "X": VPDScanner.CUEVETTE_X - marlinPrinter.X_OFFSET,
                "Y": VPDScanner.CUEVETTE_Y - marlinPrinter.Y_OFFSET,
            }
        )
        # Go in to the cuevette
        self.nonExtrudeMove({"Z": VPDScanner.CUEVETTE_Z})
        if dispense:
            self.dispenseSample()
        else:
            self.collectSample()
        # Go back up
        self.nonExtrudeMove({"Z": VPDScanner.TRAVEL_HEIGHT})

    def centerHead(self):
        """"
        Center the head (XY) over the center of the wafer.
        This function assumes the xOffset & marlinPrinter.Y_OFFSET have been set correctly
        such that the syringe tip will be over the XY center of the build area.
        """
        self.nonExtrudeMove(
            {"X": (marlinPrinter.X_MAX / 2), "Y": (marlinPrinter.Y_MAX) / 2},
            "CENTER HEAD",
        )

    def doWaferScan(self):
        """
        Centers the head over the wafer, moves tip back up.
        Moves the head to the start of the rotation, and scans 
        the wafer in concentric circles.
        """
        # Calculate the furthest point out from center (radially)
        max_radius = (VPDScanner.WAFER_DIAM / 2) - VPDScanner.EDGE_GAP
        # Divide the radius into smaller arcs to be scanned (thin cylinders radially)
        max_rotations = math.floor(max_radius / VPDScanner.DROPLET_DIAMETER)

        self.centerHead()
        self.nonExtrudeMove({"Z": VPDScanner.SCAN_HEIGHT})
        self.nonExtrudeMove(
            {
                "X": (marlinPrinter.X_MAX / 2) + max_radius,
                "F": VPDScanner.TRAVEL_FEEDRATE,
            },
            "Move to max radius",
        )
        self.extrudeMove({"E": 0, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        # self.dispenseSample()

        rotation_count = 0
        while rotation_count < max_rotations:
            # Calculate the current scan radius (from center)
            current_offset = max_radius - (rotation_count * VPDScanner.DROPLET_DIAMETER)

            self.nonExtrudeMove(
                {
                    "X": (marlinPrinter.X_MAX / 2) + current_offset,
                    "F": VPDScanner.SCANNING_MOVE_FEEDRATE,
                },
                "Move needle in.",
            )

            # Calculate relative location & move the head in a circle around the wafer center
            xRel, yRel = self.calcRelPos(
                {
                    "X": (marlinPrinter.X_MAX / 2) + current_offset,
                    "Y": marlinPrinter.Y_MAX / 2,
                },
                (marlinPrinter.X_MAX / 2),
                (marlinPrinter.Y_MAX / 2),
            )
            self.doCircle({"X": xRel, "Y": yRel})

            rotation_count += 1

        # Drop the head down a little bit to pick up the drop better
        self.nonExtrudeMove(
            {
                "Z": VPDScanner.SCAN_HEIGHT - 0.5,
                "F": VPDScanner.SCANNING_MOVE_FEEDRATE * 2,
            }
        )

        # Rotate backwards in an arc, picking up the drop
        self.doCCWArc(
            {
                "X": (marlinPrinter.X_MAX / 2) + current_offset,
                "Y": marlinPrinter.Y_MAX / 2,
                "E": self.SYRINGE_CAPACITY,
            },
            (xRel, yRel),
            current_offset,
            60,
            "arc",
        )

    def loadSyringe(self):
        """
        At the start of any given cycle, ready the system so 
        that a full syringe may be loaded in.
        """
        self.nonExtrudeMove({"Z": VPDScanner.TRAVEL_HEIGHT})
        self.nonExtrudeMove({"X": 0, "Y": 0})
        self.extrudeMove(
            {"E": self.SYRINGE_CAPACITY / 3, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE},
            "Open syringe holder.",
        )
        self.extrudeMove(
            {"E": self.sample_volume, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE},
            "Open syringe holder.",
        )
        self.beep()
        self.waitForUserInput()

    def unloadSyringe(self):
        """
        At the start of any given cycle, ready the system so 
        that a full syringe may be loaded in.
        """
        self.nonExtrudeMove({"Z": VPDScanner.TRAVEL_HEIGHT})
        self.nonExtrudeMove({"X": 0, "Y": 0})
        self.extrudeMove(
            {"E": self.SYRINGE_CAPACITY, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE},
            "Open syringe holder.",
        )
        self.beep()
        self.waitForUserInput()
        self.extrudeMove(
            {"E": 0, "F": VPDScanner.EXTRUSION_MOTOR_FEEDRATE},
            "Close syringe holder so it is ready for the next cycle.",
        )

    def endGCode(self):
        """
        End G-Code raizes the Z axis and presents the wafer.
        """
        self.relativePos()
        self.nonExtrudeMove({"Z": 15}, "Raize Z.")
        self.absPos()
        # Using 'commands.append' here avoids the adjustments for head offset, which are unnecesary here
        self.commands.append(
            f"G0 X0.0000 Y{marlinPrinter.Y_MAX} F{VPDScanner.TRAVEL_FEEDRATE} ;Present print."
        )
