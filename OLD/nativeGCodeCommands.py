#!/usr/bin/env python3
"""
All relevant native GCODE commands to be 
called by python.

Created Jul 2023
by Trevor Jehl
"""

def addDecimalPoint(*args):
    """
    GCode can have some funky issues if locations are 
    given without decimals (ie. G1 X1 instead of G1 X1.).
    This function checks for compatability and fixes if 
    possible.
    """
    result = []

    for arg in args:
        if isinstance(arg, int):  # if argument is an integer
            result.append(f"{arg}.0")
        elif isinstance(arg, float) or isinstance(arg, str):  # if argument is a float
            str_val = str(arg)
            if "." not in str_val:  # if float but doesn't have a decimal point (e.g., 5.0)
                result.append(f"{arg}.0")
            else:
                result.append(str(arg))
        else:
            return args[0]

    # If only one argument is passed, return a string
    return result[0]


def nonExtrudeMove(lst,feedrate, X=None,Y=None,Z=None):
    """
    Move the extruder without extruding.
    """
    X = addDecimalPoint(X)
    Y = addDecimalPoint(Y)
    Z = addDecimalPoint(Z)

    move = 'G0' + (f' X{X}' if X is not None else '') + (f' Y{Y}' if Y is not None else '') + (f' Z{Z}' if Z is not None else '') + f" F{feedrate}"
    
    if move != 'G0':
        lst.append(move.strip())
    
    return lst

def doCircle(lst, xCenterOffset = None, yCenterOffset = None):
    """
    Moves the printehead in a complete circle around the point
    specified by "xCenterOffset" and "yCenterOffset." Those two
    params are relative, not absolute.
    >>> doCircle([], 20, 20)
    ['G2 I20 J20']
    """
    if xCenterOffset!= None and yCenterOffset!= None:
        lst.append(f"G2 I{xCenterOffset:.4f} J{yCenterOffset:.4f}")

    elif xCenterOffset or yCenterOffset == None:
        if xCenterOffset == None:
            lst.append(f"G2 J{yCenterOffset:.4f}")
            print("second if")
        if yCenterOffset == None:
            lst.append(f"G2 I{xCenterOffset:.4f}")
            print("third if")
    return lst


def extrudeInPlace(lst, amount):
    """
    >>> extrudeInPlace([], 5)
    ['G1 E5.0']
    """
    amount = addDecimalPoint(amount)

    lst.append(f"G1 E{amount}")
    return(lst)


def relativePos(lst):
    lst.append("G91 ; Set all axes to relative")
    return lst


def absPos(lst):
    lst.append("G90 ; Set all axes to absolute")
    return lst


def writeToFile():
    pass

