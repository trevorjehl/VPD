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
        elif isinstance(arg, float):  # if argument is a float
            str_val = str(arg)
            if "." not in str_val:  # if float but doesn't have a decimal point (e.g., 5.0)
                result.append(f"{arg}.0")
            else:
                result.append(arg)
        else:
            result.append(arg)  # for all other cases, just append the original argument

    # If only one argument is passed, return a string
    return result[0] if len(result) == 1 else result


def nonExtrudeMove(lst,X=None,Y=None,Z=None):
    """
    >>> nonExtrudeMove([],1,2,3)
    ['G0 X1.0 Y2.0 Z3.0']
    >>> nonExtrudeMove([],X=1,Y=2)
    ['G0 X1.0 Y2.0']
    >>> nonExtrudeMove([],X=1,Z=3)
    ['G0 X1.0 Z3.0']
    >>> nonExtrudeMove([],Y=2,Z=3)
    ['G0 Y2.0 Z3.0']
    >>> nonExtrudeMove([],X=1)
    ['G0 X1.0']
    >>> nonExtrudeMove([],Y=2)
    ['G0 Y2.0']
    >>> nonExtrudeMove([],Z=3)
    ['G0 Z3.0']
    >>> nonExtrudeMove(['test'])
    ['test']
    """
    X, Y, Z = addDecimalPoint(X, Y, Z)

    if X != None and Y != None and Z != None:
        lst.append(f"G0 X{X} Y{Y} Z{Z}")
        return lst
    if X != None and Y != None:
        lst.append(f"G0 X{X} Y{Y}")
        return lst
    if X != None and Z != None:
        lst.append(f"G0 X{X} Z{Z}")
        return lst
    if Y!= None and Z!= None:
        lst.append(f"G0 Y{Y} Z{Z}")
        return lst
    if X!= None:
        lst.append(f"G0 X{X}")
        return lst
    if Y!= None:
        lst.append(f"G0 Y{Y}")
        return lst
    if Z != None:
        lst.append(f"G0 Z{Z}")
        return lst
    return lst


def doCircle(lst, xCenterOffset = None, yCenterOffset = None):
    """
    Moves the printehead in a complete circle around the point
    specified by "xCenterOffset" and "yCenterOffset." Those two
    params are relative, not absolute.

    >>> doCircle([], 20, 20)
    ['G2 I20.0 J20.0']
    >>> doCircle([], xCenterOffset = 39.8)
    ['G2 I39.8']
    """
    xCenterOffset, yCenterOffset = addDecimalPoint(xCenterOffset, yCenterOffset)

    if xCenterOffset!= None and yCenterOffset!= None:
        lst.append(f"G2 I{xCenterOffset} J{yCenterOffset}")
    elif xCenterOffset!= None:
        lst.append(f"G2 I{xCenterOffset}")
    elif yCenterOffset!= None:
        lst.append(f"G2 J{yCenterOffset}")
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

