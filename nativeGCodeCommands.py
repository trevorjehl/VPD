#!/usr/bin/env python3
"""
All relevant native GCODE commands to be 
called by python.

Created Jul 2023
by Trevor Jehl
"""

def nonExtrudeMove(lst,X=None,Y=None,Z=None):
    """
    >>> nonExtrudeMove([],1,2,3)
    ['G0 X1 Y2 Z3']
    >>> nonExtrudeMove([],X=1,Y=2)
    ['G0 X1 Y2']
    >>> nonExtrudeMove([],X=1,Z=3)
    ['G0 X1 Z3']
    >>> nonExtrudeMove([],Y=2,Z=3)
    ['G0 Y2 Z3']
    >>> nonExtrudeMove([],X=1)
    ['G0 X1']
    >>> nonExtrudeMove([],Y=2)
    ['G0 Y2']
    >>> nonExtrudeMove([],Z=3)
    ['G0 Z3']
    >>> nonExtrudeMove(['test'])
    ['test']
    """
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


def doCircle(lst, xCenterOffset, yCenterOffset):
    """
    >>> doCircle([], 20, 20)
    ['G2 I20 J20']
    """
    lst.append(f"G2 I{xCenterOffset} J{yCenterOffset}")
    return lst

def extrudeInPlace(lst, amount):
    """
    >>> extrudeInPlace([], 5)
    ['G1 E5']
    """
    lst.append(f"G1 E{amount}")
    return(lst)