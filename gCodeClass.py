#!/usr/bin/env python3
"""

All relevant native GCODE commands to be 
called by python.

Created Jul 2023
by Trevor Jehl

"""
import math

class marlinPrinter:
    reverseEDir = True
    X_MAX = 220
    Y_MAX = 220
    Z_MAX = 250

    def __init__(self, filename, xOffset = 0, yOffset = 0, zOffset = 0):
        """
        Creates the internal command list,
        captures filename
        """
        self.filename = filename

        self.xOffset = xOffset
        self.yOffset = yOffset
        self.zOffset = zOffset

        self.commands = [] # Create list of G-Code commands
        
        
    def sanitizeCoords(func):
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
                elif isinstance(value, float) or isinstance(value, str):  # if argument is a float or string
                    str_val = str(value)
                    if "." not in str_val:  # if float but doesn't have a decimal point (e.g., 5.0)
                        result[axis] = f"{value}.0"
                    else:
                        result[axis] = str_val
                else:
                    raise Exception ("Attempted to add decimal point to an incompatible data class.")
            
            return result
    
        def adjsutForOffset(self, coords):
            """"
            Given a 'coords' dict (ex. {'X': 10.0, 'Y': 5.0}),
            adjust for the head/tip offset.
            """
            if coords is None:
                return {'X': None, 'Y': None, 'Z': None}
            
            for axis, value in coords.items():
                if axis == "X":
                    coords['X'] = value - self.xOffset
                if axis == "Y":
                    coords['Y'] = value - self.yOffset
                if axis == 'Z':
                    coords['Z'] = value + self.zOffset
            
            return coords


        def limitDecimalPlaces(self, coords, places = 4):
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
            as strings.
            """
            coords_arg = kwargs.get('coords', None)
            args_list = list(args)

            if not coords_arg:
                for i, arg in enumerate(args):
                    if isinstance(arg, dict) and any(key in ['X', 'Y', 'Z', 'E'] for key in arg):
                        coords_arg = arg
                        args = args[:i] + args[i+1:]  # Remove the coords from args
                        break
            if not coords_arg:
                raise ValueError("coords argument not found!")
            
            coords_arg = adjsutForOffset(instance, coords_arg)
            coords_arg = addDecimalPoint(instance, coords_arg)
            coords_arg = limitDecimalPlaces(instance, coords_arg)

            args_list[i] = coords_arg  # Insert the modified coords_arg back into its original position
            args_tuple = tuple(args_list)  # Convert list back to tuple

            return func(instance, *args_tuple, **kwargs)
        
        return wrapper

    
    @sanitizeCoords
    def nonExtrudeMove(self, coords, comment = None):
        """
        Move the extruder without extruding.
        """
        # coords = self.sanitizeCoords(coords)

        move = 'G0'

        for axis, value in coords.items():
            move += f' {axis}{value}'
        if 'F' not in move:
            move+= f' F{VPDScanner.TRAVEL_FEEDRATE}'
        
        if move != 'G0':
            if comment:
                move += f" ;{comment}"
            self.commands.append(move.strip())
    

    @sanitizeCoords
    def doCircle(self, coords, comment = None):
        """
        Moves the printehead in a complete circle around the point
        specified by the coords dictionary. The values in the dictionary
        are RELATIVE, not absolute.
        >>> doCircle([], {'X': 20, 'Y': 20})
        ['G2 I20.0000 J20.0000']
        """
        # coords = self.sanitizeCoords(coords)
        if len(coords) >=3:
            raise Exception ("Passed 3 or more coordinates to the doCircle funciton.")

        move = "G2"

        for axis, value in coords.items():
            if axis == "X":
                move += f' I{value}'
            if axis == "Y":
                move += f' J{value}'
        
        if move != "G2":
            if comment:
                move += f" ; {comment}"
            self.commands.append(move.strip())


    @sanitizeCoords
    def extrudeMove(self, coords, comment = None):
        """
        >>> extrudeInPlace({'E': 5)
        ['G1 E5.0']
        """
        coord_axes = coords.keys()
        move = "G1"

        if "X" in coord_axes:
            move += (f" X{coords['X']}")
        if "Y" in coord_axes:
            move += f" Y{coords['Y']}"
        if "Z" in coord_axes:
            move += f" Z{coords['Z']}"
        if "E" in coord_axes:
            if marlinPrinter.reverseEDir:
                if float(coords['E']) >= 0:
                    move += f" E-{coords['E']}"
                elif '-' in coords['E']:
                    move += f" E{coords['E'][1:]}"
            
            else:
                move += f" E{coords['E']}"
        if 'F' in coord_axes:
            move += f" F{coords['F']}"

        if move != "G1":
            if comment: move += f" ; {comment}"
            self.commands.append(move.strip()) 
    

    @sanitizeCoords
    def setStepsPerUnit(self, coords):
        coord_axes = coords.keys()
        move = "M92"

        if "X" in coord_axes:
            move += (f" X{coords['X']}")
        if "Y" in coord_axes:
            move += f" Y{coords['Y']}"
        if "Z" in coord_axes:
            move += f" Z{coords['Z']}"
        if "E" in coord_axes:
            move += f" E{coords['E']}"

        if move != "M92":
            move += " ; Set steps per unit."
            self.commands.append(move.strip()) 


    def relativePos(self):
        self.commands.append("G91 ; Set all axes to relative")

    def absPos(self):
        self.commands.append("G90 ; Set all axes to absolute")
    
    def homeAxes(self):
        self.commands.append("G28 ; Home all axes")

    def writeToFile(self):
        """"
        To be called at the end of the routine. Writes all
        commands line by line to a .gcode file.
        """
        filename = self.filename
        if ".gcode" not in filename:
            filename += ".gcode"

        with open(filename, 'w') as file:
            for command in self.commands:
                file.write(f"{command}\n")


#################################
##### BEGIN CUSTOM COMMANDS #####
#################################


class VPDScanner(marlinPrinter):
    # PROCESS VALUES (in mm unless otherwuise noted)
    TRAVEL_FEEDRATE = 4000 # Standard is 3000
    SCANNING_MOVE_FEEDRATE = 1000 # Adjust as needed
    EXTRUSION_MOTOR_FEEDRATE = 10

    TIP_HEIGHT = 3
    TRAVEL_HEIGHT = 40 # Make sure this is well above the highest point (cuevette lid)
    DROPLET_SIZE = 10 #mm

    CUEVETTE_X = 200
    CUEVETTE_LIP_Y = 25
    CUEVETTE_Z = 10

    # Wafer specific global vars (in mm unless otherwuise noted)
    WAFER_DIAM = 101.6 # 4in wafer
    EDGE_GAP = 5 # How far in from the wafer edge to scan

    def __init__(self, filename, mL = 0.500, mm = 60):
        super().__init__(filename)
        self.mL = mL
        self.mm = mm

    def getEFeedRate(self):
        """
        Assuming the motor has 3200 steps/rev, 
        calculate the feed rate such that the command 
        'E1' dispenses exactly 1ml of solution.
        """
        mL = self.mL
        mm = self.mm

        stepsPerRotation = 3200
        stepsPerDeg = stepsPerRotation / 360
        
        gearTeeth = 30
        gearTeethPerDegree = gearTeeth /  360

        
        rackTeethPerCm = 6.36619

        mLPerMM = mL / mm
        mLPerRackTooth = (mLPerMM * 10) / rackTeethPerCm
        mLPerGearDegree = mLPerRackTooth * gearTeethPerDegree

        degreePerML = 1/mLPerGearDegree

        stepsPerML = degreePerML * stepsPerDeg

        return stepsPerML

    
    def startGCode(self):
        """
        Housekeeping -- mainly homes and then moves up.
        """
        self.commands.append("; BEGIN START GCODE")
        self.commands.append("G21 ; set units to millimeters")
        self.commands.append("M82 ;absolute extrusion mode")
        self.commands.append("M302 S0; always allow extrusion (disable checking)")
        self.commands.append("G92 E0 ; Reset Extruder")

        self.homeAxes()
        self.absPos()
        self.commands.append("G92 E0 X0 Y0 Z0; Set home position")
        
        # Set appropriate e_steps
        e_steps = self.getEFeedRate()
        self.setStepsPerUnit({'E': e_steps})
        
        self.nonExtrudeMove({'Z': 2.0}, "Move up to prevent scratching.") #Set XYZ feedrate, move up

        self.commands.append("; END START GCODE")


    def calcRelPos(self, xAbs, yAbs, xPoint, yPoint):
        """
        Given a point in space (xPoint, yPoint) and
        the current absolute position, calculate the
        XY vector to travel from the abs to the point.
        """
        return (xPoint - xAbs, yPoint - yAbs)  


    def collectSample(self, volume):
        """"
        Assume needle tip is in location where ready to 
        collect, collect the volume.
        """
        self.extrudeMove({'E': -volume/2, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.extrudeMove({'E': volume/2, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.extrudeMove({'E': -volume, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})


    def dispenseSample(self, volume):
        """"
        Assume needle tip is in location where ready to 
        dispense, dispense the volume.
        """
        self.extrudeMove({'E': volume, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.extrudeMove({'E': -volume/2, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.extrudeMove({'E': volume/2, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})


    def useCuevette(self, dispense: bool):
        """
        If dispense is true, will dispense sample. Otherwise 
        will collect sample.
        Using the cuevette measurements (found in
        global variables), move up, move over, move down,
        and deposit the scanned droplet.
        """
        # move up
        self.nonExtrudeMove({'Z': VPDScanner.TRAVEL_HEIGHT})
        #move over cuevette
        self.nonExtrudeMove({'X': VPDScanner.CUEVETTE_X, 'Y': VPDScanner.CUEVETTE_LIP_Y })
        #Go in to the cuevette
        self.nonExtrudeMove({'Z': VPDScanner.CUEVETTE_Z})
        if dispense:
            self.dispenseSample(self.mL)
        else:
            self.collectSample(self.mL)
        # Go back up
        self.nonExtrudeMove({'Z': VPDScanner.TRAVEL_HEIGHT})
        

    def centerHead(self):
        self.nonExtrudeMove({'Z': 3}, "BEGIN CENTER HEAD")
        self.nonExtrudeMove({'X': (marlinPrinter.X_MAX/2), 'Y': (marlinPrinter.Y_MAX)/2})
        self.nonExtrudeMove({'Z': 1}, "END CENTER HEAD")
    
    def doWaferScan(self):
        """
        Centers the head over the wafer, moves tip back up.
        Moves the head to the start of the rotation, and scans 
        the wafer in concentric circles.
        """
        
        max_radius = (VPDScanner.WAFER_DIAM/2) - VPDScanner.EDGE_GAP
        max_rotations = math.floor(max_radius/ VPDScanner.DROPLET_SIZE)

        self.centerHead() # Keep pos in absolute
        self.nonExtrudeMove({'Z': VPDScanner.TIP_HEIGHT})

        rotation_count = 0 

        self.extrudeMove({'E': self.mL, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})

        while rotation_count < max_rotations:
            current_offset = max_radius - (rotation_count * VPDScanner.DROPLET_SIZE) 

            self.nonExtrudeMove({'X': (marlinPrinter.X_MAX/2) + current_offset, 'F': VPDScanner.SCANNING_MOVE_FEEDRATE}, "Move needle in.")

            xRel, yRel = self.calcRelPos((marlinPrinter.X_MAX/2) + current_offset, marlinPrinter.Y_MAX/2, (marlinPrinter.X_MAX/2), (marlinPrinter.Y_MAX / 2))
            self.doCircle({'X': xRel, 'Y': yRel})

            rotation_count += 1
        
        self.extrudeMove({'E': -1 * float(self.mL), 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
    

    def endGCode(self):
        """
        End G-Code raizes the Z axis and presents the wafer.
        """
        self.relativePos()
        self.nonExtrudeMove({'Z': 10}, "Raize Z.")
        self.absPos()
        self.nonExtrudeMove({'X': 0, 'Y': marlinPrinter.Y_MAX}, "Present print.")
