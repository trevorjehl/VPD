# A Guide To More In-Depth Code Modification Using `TEMPLATE.py`

If you have not read the other code documentation, please do so ([README.md](/README.md), [CUSTOM_SCAN.md](CUSTOM_SCAN.md)).

This document discusses the structure, design, and usage of `TEMPLATE.py` for more granular modificaitons to the scanning protocols than can be accomplished by only changing pre-existing paramaters and printer actions.

## Basic Structure
This section provides an overview of the function and design of the `TEMPLATE.py` file.

The file is divided into two Python classes: `marlinPrinter` & `VPDScanner`. Since the VPD scanner is an abstraction of the functions available on a consumer 3D printer, it was useful to split the functions available into these two categories.

The `VPDScanner`is the child class of `marlinPrinter`, inheriting its functions and parameters.

1. ### `marlinPrinter` Class

- The `marlinPrinter` class contains an assortment of G-Code commands that are useful for the purposes of this project. By containing all of these functions within a class (as opposed to regular functions in a Python script), we are able to attach the G-Code commands to the class object instead, which eliminates the need to write to a file after every command or to pass around a list of commands from function to function.

    1. ### `coords` / Coordinates Dictionary 
        1. #### Structure
            - Most of the functions use coords argument, which is formatted as a dictionary with the axis as the key and value for each respective axis (ex `coords = {'X': 10.0, 'F': 1000, 'E': 0.1}`)
            - There are multiple reasons to use a dictionary instead of a `math` vector object or list. Using a dictionary allows for a combination of verbosity and concision that is appealing for enhancing readibility of the code.
                - Since the object is a dictionary, only the axes used need to be defined. This eliminates the need to contain unnecesary `None` or `0` values for unused axes, which would be neccesary in a string or vector.
                - However, each axis does have to be defined for each call of the `coords` value. This decision means the code is more readable for someone unfamiliar with the program, as well as reducing the likelihood of errors. 
                    - Consider the difference between `[0.105, None, None, 1]` and `{'E': 0.105, 'X': 1}`. In the latter example it is clear which value is assigned to each axis.
        2. #### `@sanitizeCoords` Wrapper
            - To minimize the likelihood of errors, a wrapper function was written which controls the style and formatting of `coords ` variables passed into functions. `@sanitizeCoords` accomplishes three main functions.
                1. `addDecimalPoint`
                    - Since G-code can sometimes have issues if commands are passed in without decimal points (such as 3 instea of 3.0), this function adds a decimal point to all values.
                2. `adjsutForOffset`
                    - Since the new scanhead is in a different point in space from the original printhead, the same movement command will make the syringe tip move to a different point in space. We still want the printhead to move to the defined point, so we calculate and/or measure the offset by using a known reference point or by referencing CAD.
                3. `limitDecimalPlaces`
                    - Although we want decimal points in all commands, we do not want exess decimal points. The system has a limited amount of granularity in space (it can only move in a limited interval). Thus providing too many decimal places can cause errors too, so this function limits decimal places to 4.
            - **Cases when we do not want to account for head offset:** 
                - Sometimes accounting for the head offset can cause issues in the code.
                    1. For example, adjusting for the head offset when scanning the wafer will cause issues. Since the rotation move in G-code is defined by the printhead's relative position to the circle's center, adjusting for the printhead on every rotation will cause a gradual shift in the location of the circle's center.
                    2.  When using the Cuevette, we want to use absolute coordinates, not coordinates adjusted for the printhead. Since the location of the cuevette is determined experimentally, adjusting for the head offset will make the printhead go to the wrong point in space.
                - `undoHeadOffset` will correct for this issue. Make sure to be careful where and when you adjust for the new printhead.

2. ### `VPDScanner` Class

    - As noted earlier, this class inherits (is a child class of) the `marlinPrinter` class. Functions in this class are either specifically for the scanner or build on & combine simple G-code functions to create a movemement pattern specifically suited for VPD scanning.

    - Most functions are self-explanatory and documented sufficiently within the code. This section will highlight any particularly confusing portions of this class.

    1. ### `calcEFeedRate`
        - This function allows for easy changes of the syringe used for the scan droplet. Since the 'E' paramater of the `coords` dict is in mL, some calculations must be done to calculate how much the motor must move per mL. This function accomplishes that task. The printer is told of this value in the start G-code.
    2. ### `doWaferScan`
        - This function is designed to scan a wafer of specified size. Since it is a complicated series of actions, this section walks through each of those steps sequentally.
            1. Calculate the `max_radius `and `max_rotations`.
                - The max radius is the given radius of the wafer without the `EDGE_GAP`, to ensure that the syringe doesnt hit the edges and that the drop does not fall off of the wafer.
                - The max rotations are calculated by dividing the max radius by the droplet size, and taking the lowest integer value of the quotient, eliminating any bugs resulting from partial scan arcs from decimals.
            2. Center the printhead, move the printhead to the scanning height.
            3. Move to the max radius, dispense solution.
            4. While loop: scanning arcs.
                - For each rotation, the printhead will move to the radius of the scan arc. The program then calculates the position of the center of the wafer relative to the printhead (neccesary for G-code arcs), and executes a circular move.
                - After the move is completed, the program increases the `rotation_count` until the maximum rotations are reached.
            5. Pick up the scan droplet.
                - Since the scan droplet tends to trail behind the syringe nozzle, this section does a counter clockwise rotation backwards while pulling the syringe plunger up. This is in an attempt to recover as much of the drop as possible.

## Making & Modifying Functions
