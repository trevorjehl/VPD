#!/usr/bin/env python3
"""
This file is designed to list out a set of custom 
G-Code commands for use in wafer scanning with a 
3D printer.

Created Jul 2023
by Trevor Jehl
"""

__author__ = "Trevor Jehl"
__version__ = "0.1.0"
# __license__ = "MIT"

import os
import math
from nativeGCodeCommands import *

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

#################################
########### BEGIN CODE ##########
#################################

def compensateNozzleOffset(vector):
    """"
    Given a point in absolute space (vector),
    compensate for the syringe tip offset and 
    return the adjusted new vector.
    """
    pass


def startGCode(lst):
    """
    Housekeeping -- mainly homes and then moves up.
    """
    lst.append("; BEGIN START GCODE")

    lst.append("G21 ; set units to millimeters")
    lst.append("M82 ;absolute extrusion mode")
    lst.append("M302 S0; always allow extrusion (disable checking)")
    lst.append("G92 E0 ; Reset Extruder")
    lst.append("G28 ; Home all axes")
    lst.append("G90; Absolute positioning")
    lst.append("G92 E0 X0 Y0 Z0; Set home position")
    #Set extruder feedrate
    lst.append(f"M203 E{E_FEEDRATE}")
    #Set XYZ feedrate, move up
    # lst.append(f"M203 X{TRAVEL_FEEDRATE} Y{TRAVEL_FEEDRATE} Z{TRAVEL_FEEDRATE}")
    lst.append(f"G1 Z2.0; Move up to prevent scratching")

    lst.append("; END START GCODE")

    return lst


def centerHead(lst):
    lst.append("; BEGIN CENTER HEAD")
    nonExtrudeMove(lst, TRAVEL_FEEDRATE, Z=3)
    nonExtrudeMove(lst, TRAVEL_FEEDRATE, X=(X_MAX/2), Y=(Y_MAX)/2)
    nonExtrudeMove(lst, TRAVEL_FEEDRATE, Z=1)

    lst.append("; END CENTER HEAD")

    return lst


def calcRelPos(xAbs, yAbs, xPoint, yPoint):
    """
    Given a point in space (xPoint, yPoint) and
    the current absolute position, calculate the
    XY vector to travel from the abs to the point.
    """
    return (xPoint - xAbs, yPoint - yAbs)

def depositSample(lst):
    """
    Using the cuevette measurements (found in
    global variables), move up, move over, move down,
    and deposit the scanned droplet.
    """
    # move up
    nonExtrudeMove(lst, TRAVEL_FEEDRATE, Z = TRAVEL_HEIGHT)
    #move over cuevette
    nonExtrudeMove(lst, TRAVEL_FEEDRATE, X = CUEVETTE_X, Y = (CUEVETTE_LIP_Y + 3))
    #Go in to the cuevette
    nonExtrudeMove(lst, TRAVEL_FEEDRATE, Z = CUEVETTE_BOTTOM_HEIGHT)
    # Go back up
    nonExtrudeMove(lst, TRAVEL_FEEDRATE, X = CUEVETTE_X, Y = (CUEVETTE_LIP_Y + 3))
    
    return lst

def doWaferScan(lst):
    """
    Centers the head over the wafer, moves tip back up.
    Moves the head to the start of the rotation, and scans 
    the wafer in concentric circles.
    """
    rotation_count = 0 
    max_radius = (WAFER_DIAM/2) - EDGE_LENGTH
    max_rotations = math.floor(max_radius/ DROPLET_SIZE)

    centerHead(lst) # Keep pos in absolute
    nonExtrudeMove(lst, TRAVEL_FEEDRATE, Z=TIP_HEIGHT)

    while rotation_count < max_rotations:
        current_offset = max_radius - (rotation_count * DROPLET_SIZE) 

        # Move the head in a bit.
        lst.append(";Move the head in.")
        nonExtrudeMove(lst,  E_FEEDRATE, X=(X_MAX/2) + current_offset)

        # GCodeCircle(lst, ((X_MAX/2) + current_offset), Y_MAX/2, (X_MAX/2), (Y_MAX / 2))
        xRel, yRel = calcRelPos((X_MAX/2) + current_offset, Y_MAX/2, (X_MAX/2), (Y_MAX / 2))

        doCircle(lst, xRel, yRel)

        rotation_count += 1
    
    return lst


def endGCode(lst):
    """
    End G-Code raizes the Z axis and presents the wafer.
    """
    lst.append("G91 ;Relative positioning")
    lst.append("G1 Z10 ; Raise Z")
    lst.append("G90 ;Absolute positioning")
    lst.append(f"G1 X0 Y{Y_MAX} ;Present print")

    return lst


def write_to_gcode(lst, filename):
    """
    At the end of usage, write all commands to a G-code file
    in the local directory of filename "filename."
    """
    # "w" indicates write the new file, "+" Plus sign indicates
    # both read and write for Python create file operation.
    f= open(filename + ".gcode","w+")
    for command in lst:
        f.write(command + "\n")
    
    # Close the file, writing the lines.
    f.close()


# def GCodeCircle(lst, x_start, y_start, x_center, y_center):
#     """
#     Since arc movements are not universally interpreted, 
#     creates a fragmented circular movement system by 
#     using linear moves to approximate a circle.
#     """ 
#     # Calculate current angles
#     start_angle = math.atan2(y_start - y_center, x_start - x_center)

#     radius = math.sqrt((x_start - x_center)**2 + (y_start - y_center)**2)
#     # print("rad" + str(radius))
    
#     segments = 1
#     angle_step = (2 * math.pi) / segments
#     # Calculate actual path length
#     act_path_length = angle_step * radius
#     # print("act path length: " + str(act_path_length))

#     # Optimzie segment length
#     while (MAX_PATH_LENGTH - act_path_length) < (MAX_PATH_LENGTH - (MAX_PATH_LENGTH*0.1)):
#         segments += 1
#         angle_step = (2 * math.pi) / segments
#         act_path_length = angle_step * radius

#     # '+1' ensures the circle closes
#     for segment in range(segments + 1):
#         # Calculate segment angle
#         segment_angle = start_angle - angle_step * segment

#         # Calculate the segment endpoint
#         dx = radius * math.cos(segment_angle)
#         dy = radius * math.sin(segment_angle)
        
#         x = x_center + dx
#         y = y_center + dy

#         #Create the G-Code for the segment
#         nonExtrudeMove(lst, f"{x:.4f}", f"{y:.4f}")

#     return lst