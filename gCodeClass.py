#!/usr/bin/env python3
"""
All relevant native GCODE commands to be 
called by Python.

Created Jul 2023
by Trevor Jehl
Stanford Nanofabrication Facility 2023
"""
import math

class marlinPrinter:
    X_MAX = 235
    Y_MAX = 235
    Z_MAX = 250

    def __init__(self, filename, xOffset = -8.3, yOffset = 17.02, zOffset = 0):
        """
        Creates the internal command list, captures the gcode filename to write to,
        defines the nozzle offset for the printer.
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
                    else: # if the number is already formatted correctly
                        result[axis] = str_val
                else:
                    raise Exception ("Attempted to add decimal point to an incompatible data class.")
            
            return result
    

        def adjsutForOffset(self, coords):
            """"
            Given a 'coords' dict (ex. {'X': 10.0, 'Y': 5.0}),
            adjust for the head/tip/nozzle offset.
            """
            if coords is None:
                return {'X': None, 'Y': None, 'Z': None}
            
            for axis, value in coords.items():
                if axis == "X":
                    coords['X'] = value + self.xOffset
                if axis == "Y":
                    coords['Y'] = value + self.yOffset
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
            # retrive anything called 'coords' from a function's input
            coords_arg = kwargs.get('coords', None)
            # get all the arguments passed into a function
            args_list = list(args)

            # If no 'coords' arg found, then 
            if not coords_arg:
                # Iterate through each argument to check for a dictionary containing position related keys
                for i, arg in enumerate(args):
                    if isinstance(arg, dict) and any(key in ['X', 'Y', 'Z', 'E', 'F'] for key in arg):
                        coords_arg = arg
                        # Remove the found coordinates dictionary from the arguments list
                        args = args[:i] + args[i+1:]  # Remove the coords from args
                        break # stop looking
            
            if not coords_arg: # Raise an error if 'coords' argument is still not found after the checks
                raise ValueError("coords argument not found!")
            
            coords_arg = adjsutForOffset(instance, coords_arg)
            coords_arg = addDecimalPoint(instance, coords_arg)
            coords_arg = limitDecimalPlaces(instance, coords_arg)

            args_list[i] = coords_arg  # Insert the modified coords_arg back into its original position
            args_tuple = tuple(args_list)  # Convert list back to tuple (it is initially a tuple)

            return func(instance, *args_tuple, **kwargs)
        
        return wrapper

    
    @sanitizeCoords
    def nonExtrudeMove(self, coords, comment = None):
        """
        Move the extruder without extruding. E units are in mL.
        """
        # coords = self.sanitizeCoords(coords)

        move = 'G0' # base command

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
                fixedX = float(value) - self.xOffset
                move += f' I{fixedX:.4f}'
            if axis == "Y":
                fixedY = float(value) - self.yOffset
                move += f' J{fixedY:.4f}'
        
        if move != "G2":
            if comment:
                move += f" ; {comment}"
            self.commands.append(move.strip())


    @sanitizeCoords
    def extrudeMove(self, coords, comment = None):
        """
        Move any set of X,Y,Z,E axes. E axis is ALWAYS 
        absolute positioning. E units are in mL. Specify
        'F' in the coords dict to determine the feedrate.
        >>> extrudeInPlace({'E': 5)
        ['G1 E5.0']
        """
        # self.commands.append('M83; Set E to relative positioning')
        self.commands.append('M82; Set E to absolute positioning')

        coord_axes = coords.keys()
        move = "G1"

        for axis, value in coords.items():
            move += f' {axis}{value}'
        if 'F' not in move:
            move+= f' F{VPDScanner.TRAVEL_FEEDRATE}'

        if move != "G1":
            if comment: move += f" ; {comment}"
            self.commands.append(move.strip()) 
    

    @sanitizeCoords
    def setStepsPerUnit(self, coords):
        coord_axes = coords.keys()
        move = "M92"

        for axis, value in coords.items():
            move += f' {axis}{value}'

        if move != "M92":
            move += " ; Set steps per unit."
            self.commands.append(move.strip()) 


    def relativePos(self):
        self.commands.append("G91 ; Set all axes to relative")

    def absPos(self):
        self.commands.append("G90 ; Set all axes to absolute")
    
    def homeAxes(self):
        self.commands.append("G28 ; Home all axes")

    def wait(self, seconds = 0.5):
        self.commands.append(f"G4 S{seconds:.4f}")
    
    def waitForUserInput(self):
        self.commands.append("M0 ; Stop and wait")
    
    def waitForMovesToComplete(self):
        self.commands.append('M400')

    def beep(self, sec = 0.2):
        """
        Beep for 'sec' seconds.
        """
        self.waitForMovesToComplete()
        self.commands.append(f'M300 P{(sec*1000):.4f} ; Beep.')

    def writeToFile(self):
        """"
        To be called at the end of the routine. Writes all
        commands line by line to a .gcode file. Filename defined
        when creating class instance.
        """
        filename = self.filename
        if ".gcode" not in filename:
            filename += ".gcode"

        with open(filename, 'w') as file:
            for command in self.commands:
                file.write(f"{command}\n")


#####################################################
#####################################################
############### BEGIN CUSTOM COMMANDS ###############
#####################################################
#####################################################


class VPDScanner(marlinPrinter):
    # PROCESS VALUES (in mm unless otherwuise noted)
    TRAVEL_FEEDRATE = 4000 # Standard is 3000
    SCANNING_MOVE_FEEDRATE = 1000 # Adjust as needed
    EXTRUSION_MOTOR_FEEDRATE = 10

    SCAN_HEIGHT = 3 # How high from the z-stop should the tip be to scan?
    TRAVEL_HEIGHT = 40 # Make sure this is well above the cuevette lid height
    DROPLET_SIZE = 3 #mm

    CUEVETTE_X = 200
    CUEVETTE_Y = 25
    CUEVETTE_Z = 10

    # Wafer specific global vars (in mm unless otherwuise noted)
    WAFER_DIAM = 101.6 # 4in wafer
    EDGE_GAP = 5 # How far in from the wafer edge to scan

    # Only adjust the paramaters below if the physical gears are modified
    RACK_TEETH_PER_CM = 6.36619
    GEAR_TEETH = 30

    SYRINGE_CAPACITY = 0.500
    SYRINGE_LENGTH = 60

    def __init__(self, filename, sample_volume, **kwargs):
        """"
        Creates a VPD scanner class object. Filename will write the
        gcode to that file. Sample_volume defines how much liquid 
        the system will use during the scan
        """
        super().__init__(filename, **kwargs)
        self.sample_volume = sample_volume


    def calcEFeedRate(self):
        """
        Assuming the motor has 3200 steps/rev, 
        calculate the feed rate such that the command 
        'E1' dispenses exactly 1ml of solution.
        """
        mL = VPDScanner.SYRINGE_CAPACITY
        mm = VPDScanner.SYRINGE_LENGTH

        # print(f"ml = {mL}")
        # print(f"mm = {mm}")

        stepsPerRotation = 3200
        stepsPerDeg = stepsPerRotation / 360
        
        gearTeeth = VPDScanner.GEAR_TEETH
        gearTeethPerDegree = gearTeeth /  360
        
        rackTeethPerCm = VPDScanner.RACK_TEETH_PER_CM

        mLPerMM = mL / mm
        mLPerRackTooth = (mLPerMM * 10) / rackTeethPerCm
        mLPerGearDegree = mLPerRackTooth * gearTeethPerDegree

        degreePerML = 1/mLPerGearDegree

        stepsPerML = degreePerML * stepsPerDeg

        # print(f"stepsPerML = {stepsPerML}")

        return stepsPerML
    
    def returnTrueXY(coords):
        """
        Some moves must be done in terms of the true XY
        position without adjusting for the head offset. These moves
        include the circular scan rotations as well as the cuevette moves.
        This function subtracts the head offsets to the coords so the effect 
        is that the true coords are written to the gcode.
        """
        pass


    
    def startGCode(self):
        """
        Housekeeping -- mainly homes and then moves up.
        """
        self.commands.append("; BEGIN START GCODE")
        self.commands.append("G21 ; set units to millimeters")
        self.commands.append("M82 ;absolute extrusion mode")
        self.commands.append("M302 S0; always allow extrusion (disable temp/length checking)")
        self.commands.append("G92 E0 ; Reset Extruder")

        self.homeAxes()
        self.absPos()
        self.commands.append("G92 E0 X0 Y0 Z0; Set home position")
        
        # Set appropriate e_steps
        e_steps = self.calcEFeedRate()
        self.setStepsPerUnit({'E': e_steps})
        
        self.nonExtrudeMove({'Z': 2.0}, "Move up to prevent scratching.") #Set XYZ feedrate, move up
        self.commands.append(";")
        self.commands.append("; END START GCODE")
        self.commands.append(";")


    def calcRelPos(self, xAbs, yAbs, xPoint, yPoint):
        """
        Given a point in space (xPoint, yPoint) and
        the current absolute position, calculate the
        XY vector to travel from the abs to the point.
        """
        return (xPoint - xAbs, yPoint - yAbs)  


    def collectSample(self, volume = None):
        """"
        Assume needle tip is in location where ready to 
        collect, collect the volume.
        """
        if not volume:
            volume = self.sample_volume
        
        self.extrudeMove({'E': volume/2, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.wait()
        self.extrudeMove({'E': 0, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.wait()
        self.extrudeMove({'E': volume, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.wait()


    def dispenseSample(self, volume = None):
        """"
        Assume needle tip is in location where ready to 
        dispense, dispense the volume.
        """
        if not volume:
            volume = self.sample_volume
        
        self.extrudeMove({'E': 0, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.wait()
        self.extrudeMove({'E': volume/2, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
        self.wait()
        self.extrudeMove({'E': 0, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})
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
        self.nonExtrudeMove({'Z': VPDScanner.TRAVEL_HEIGHT})
        #move over cuevette
        self.nonExtrudeMove({'X': VPDScanner.CUEVETTE_X - self.xOffset , 'Y': VPDScanner.CUEVETTE_Y - self.yOffset})
        #Go in to the cuevette
        self.nonExtrudeMove({'Z': VPDScanner.CUEVETTE_Z})
        if dispense:
            self.dispenseSample()
        else:
            self.collectSample()
        # Go back up
        self.nonExtrudeMove({'Z': VPDScanner.TRAVEL_HEIGHT})
        

    def centerHead(self):
        self.nonExtrudeMove({'X': (marlinPrinter.X_MAX/2), 'Y': (marlinPrinter.Y_MAX)/2}, "CENTER HEAD")
    

    def doWaferScan(self):
        """
        Centers the head over the wafer, moves tip back up.
        Moves the head to the start of the rotation, and scans 
        the wafer in concentric circles.
        """
        # Calculate the furthest point out from center (radially)
        max_radius = (VPDScanner.WAFER_DIAM/2) - VPDScanner.EDGE_GAP
        # Divide the radius into smaller arcs to be scanned
        max_rotations = math.floor(max_radius / VPDScanner.DROPLET_SIZE)

        self.centerHead()
        self.nonExtrudeMove({'Z': VPDScanner.SCAN_HEIGHT})
        self.dispenseSample()

        rotation_count = 0 
        while rotation_count < max_rotations:
            # Calculate the current scan radius (from center)
            current_offset = max_radius - (rotation_count * VPDScanner.DROPLET_SIZE) 

            self.nonExtrudeMove({'X': (marlinPrinter.X_MAX/2) + current_offset, 'F': VPDScanner.SCANNING_MOVE_FEEDRATE}, "Move needle in.")

            # Calculate relative location & move the head in a circle around the wafer center
            xRel, yRel = self.calcRelPos((marlinPrinter.X_MAX/2) + current_offset, marlinPrinter.Y_MAX/2, (marlinPrinter.X_MAX/2), (marlinPrinter.Y_MAX / 2))
            self.doCircle({'X': xRel, 'Y': yRel})

            rotation_count += 1
        
        # Pick the sample back up
        self.extrudeMove({'E': self.sample_volume, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE})


    def loadSyringe(self):
        """
        At the start of any given cycle, ready the system so 
        that a full syringe may be loaded in.
        """
        self.nonExtrudeMove({'X': 0, 'Y': 0, 'Z': VPDScanner.TRAVEL_HEIGHT})
        self.extrudeMove({'E': self.sample_volume, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE}, 'Open syringe holder.')
        self.beep()
        self.waitForUserInput()

    def unloadSyringe(self):
        """
        At the start of any given cycle, ready the system so 
        that a full syringe may be loaded in.
        """
        self.nonExtrudeMove({'X': 0, 'Y': 0, 'Z': VPDScanner.TRAVEL_HEIGHT})
        self.extrudeMove({'E': self.SYRINGE_CAPACITY, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE}, 'Open syringe holder.')
        self.beep(0.3)
        self.waitForUserInput()
        self.extrudeMove({'E': 0, 'F': VPDScanner.EXTRUSION_MOTOR_FEEDRATE}, 'Close syringe holder so it is ready for the next cycle.')
    

    def endGCode(self):
        """
        End G-Code raizes the Z axis and presents the wafer.
        """
        self.relativePos()
        self.nonExtrudeMove({'Z': 15}, "Raize Z.")
        self.absPos()
        self.nonExtrudeMove({'X': 0, 'Y': marlinPrinter.Y_MAX}, "Present print.")
