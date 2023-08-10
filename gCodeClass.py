#!/usr/bin/env python3
"""
All relevant native GCODE commands to be 
called by python.

Created Jul 2023
by Trevor Jehl
"""
#################################
### CUSTOMIZE VARIABLES BELOW ###
#################################

#ENDER 3 CONSTRAINTS
X_MAX = 220
Y_MAX = 220
Z_MAX = 250

# PROCESS VALUES (in mm unless otherwuise noted)
TRAVEL_FEEDRATE = 5000 # Standard is 1125
E_FEEDRATE = 1500 # Adjust as needed
DISPENSE_FEEDRATE = 1000 # Feedrate for moving the syringe
DROPLET_SIZE = 1
TIP_HEIGHT = 3
TRAVEL_HEIGHT = 40 # Make sure this is well above the highest point (cuevette lid)

CUEVETTE_X = 200
CUEVETTE_LIP_Y = 25
CUEVETTE_BOTTOM_HEIGHT = 10

# DEPRECIATED MAX_PATH_LENGTH = 1 # How long (in mm) should the head linearly travel?

# Wafer specific global vars (in mm unless otherwuise noted)
WAFER_DIAM = 101.6 # 4in wafer
EDGE_LENGTH = 5 # How far in from the wafer edge to scan

###########################
###########################
###########################

import math

class marlinGCode:

    def __init__(self, filename, xOffset = 0, yOffset = 0):
        """
        Creates the internal command list,
        captures filename
        """
        self.commands = []
        self.filename = filename
        self.xOffset = xOffset
        self.yOffset = yOffset

    def sanitizeCoords(func):
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
            
            return coords

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
            print(args)
            args_list = list(args)

            if not coords_arg:
                for i, arg in enumerate(args):
                    if isinstance(arg, dict) and any(key in ['X', 'Y', 'Z'] for key in arg):
                        coords_arg = arg
                        args = args[:i] + args[i+1:]  # Remove the coords from args
                        break
            if not coords_arg:
                raise ValueError("coords argument not found!")
            
            print(coords_arg)
            
            coords_arg = adjsutForOffset(instance, coords_arg)
            coords_arg = addDecimalPoint(instance, coords_arg)
            coords_arg = limitDecimalPlaces(instance, coords_arg)


            print(f"args: {args}")
            print(f"kwargs: {kwargs}")
            print(f"sanitized_coords: {coords_arg}")

            args_list[i] = coords_arg  # Insert the modified coords_arg back into its original position
            args_tuple = tuple(args_list)  # Convert list back to tuple

            print(args_tuple)
            return func(instance, *args_tuple, **kwargs)
        
        return wrapper


    @sanitizeCoords
    def nonExtrudeMove(self, coords, feedrate = TRAVEL_FEEDRATE):
        """
        Move the extruder without extruding.
        """
        # coords = self.sanitizeCoords(coords)

        move = 'G0'

        for axis, value in coords.items():
            move += f' {axis}{value}'
        move += f" F{feedrate}"
        
        if move != 'G0':
            self.commands.append(move.strip())
    
    @sanitizeCoords
    def doCircle(self, coords):
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
                move += f' I{value}'
        
        if move != "G2":
            self.commands.append(move.strip())


    def extrudeInPlace(self, amount):
        """
        >>> extrudeInPlace([], 5)
        ['G1 E5.0']
        """
        amount = self.addDecimalPoint(amount)

        move = f"G1 E{amount}"
        self.commands.append(move.strip())


    def relativePos(self):
        self.commands.append("G91 ; Set all axes to relative")


    def absPos(self):
        self.commands.append("G90 ; Set all axes to absolute")


    def writeToFile(self):
        filename = self.filename
        if ".gcode" not in filename:
            filename += ".gcode"

        with open(filename, 'w') as file:
            for command in self.commands:
                file.write(f"{command}\n")


#################################
##### BEGIN CUSTOM COMMANDS #####
#################################


class CustomGCodeCommands(marlinGCode):
    def __init__(self, filename):
        super().__init__(filename)
    
    def startGCode(self):
        """
        Housekeeping -- mainly homes and then moves up.
        """
        self.commands.append("; BEGIN START GCODE")
        self.commands.append("G21 ; set units to millimeters")
        self.commands.append("M82 ;absolute extrusion mode")
        self.commands.append("M302 S0; always allow extrusion (disable checking)")
        self.commands.append("G92 E0 ; Reset Extruder")
        self.commands.append("G28 ; Home all axes")
        self.commands.append("G90; Absolute positioning")
        self.commands.append("G92 E0 X0 Y0 Z0; Set home position")
        #Set extruder feedrate
        self.commands.append(f"M203 E{E_FEEDRATE}")
        #Set XYZ feedrate, move up
        self.commands.append(f"G1 Z2.0; Move up to prevent scratching")

        self.commands.append("; END START GCODE")

    def calcRelPos(self, xAbs, yAbs, xPoint, yPoint):
        """
        Given a point in space (xPoint, yPoint) and
        the current absolute position, calculate the
        XY vector to travel from the abs to the point.
        """
        return (xPoint - xAbs, yPoint - yAbs)  
    
    def depositSample(self):
        """
        Using the cuevette measurements (found in
        global variables), move up, move over, move down,
        and deposit the scanned droplet.
        """
        # move up
        self.nonExtrudeMove({'Z': TRAVEL_HEIGHT})
        #move over cuevette
        self.nonExtrudeMove({'X': CUEVETTE_X, 'Y': (CUEVETTE_LIP_Y + 3)})
        #Go in to the cuevette
        self.nonExtrudeMove({'Z': CUEVETTE_BOTTOM_HEIGHT})
        # Go back up
        self.nonExtrudeMove({'X': CUEVETTE_X, 'Y':(CUEVETTE_LIP_Y + 3)})
        
    def centerHead(self):
        self.commands.append("; BEGIN CENTER HEAD")
        self.nonExtrudeMove({'Z': 3})
        self.nonExtrudeMove({'X': (X_MAX/2), 'Y': (Y_MAX)/2})
        self.nonExtrudeMove({'Z': 1})
        self.commands.append("; END CENTER HEAD")
    
    def doWaferScan(self):
        """
        Centers the head over the wafer, moves tip back up.
        Moves the head to the start of the rotation, and scans 
        the wafer in concentric circles.
        """
        rotation_count = 0 
        max_radius = (WAFER_DIAM/2) - EDGE_LENGTH
        max_rotations = math.floor(max_radius/ DROPLET_SIZE)

        self.centerHead() # Keep pos in absolute
        self.nonExtrudeMove({'Z': TIP_HEIGHT})

        while rotation_count < max_rotations:
            current_offset = max_radius - (rotation_count * DROPLET_SIZE) 

            # Move the head in a bit.
            self.commands.append(";Move the head in.")
            self.nonExtrudeMove({'X': (X_MAX/2) + current_offset}, E_FEEDRATE)

            xRel, yRel = self.calcRelPos((X_MAX/2) + current_offset, Y_MAX/2, (X_MAX/2), (Y_MAX / 2))

            self.doCircle({'X': xRel, 'Y': yRel})

            rotation_count += 1
    

    def endGCode(self):
        """
        End G-Code raizes the Z axis and presents the wafer.
        """
        self.commands.append("G91 ;Relative positioning")
        self.commands.append("G1 Z10 ; Raise Z")
        self.commands.append("G90 ;Absolute positioning")
        self.commands.append(f"G1 X0 Y{Y_MAX} ;Present print")
