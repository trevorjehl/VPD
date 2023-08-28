# Creating Custom Scan Routines
The VPD scanning program has been written with the intention of being easy to change for anyone with minimal programming experience. The types of modifications that can be made can be broken down into three subcategories:
1. Instance Parameters
2. Class parameters
3. Actions

This document outlines how (and when) to make these modifications.

| Category                | Sub-category / Parameter             | Description |
|-------------------------|-------------------------------------|-------------|
| **Instance Parameters** | marlinPrinter: `filename`            | Filename to which gcode commands are written. Can have .gcode extension or not. |
|                         | VPDScanner: `sample_volume`          | Determines the droplet volume for scanning the wafer. |
| **Class Parameters**    | **Printer Parameters**              |             |
|                         | *_OFFSET Parameters*                | Specify offsets for printer to compensate for non-standard printhead. Parameters include `X_OFFSET`, `Y_OFFSET`, `Z_OFFSET`. |
|                         | *_MAX Parameters*                   | Specify the maximum print space dimensions. Includes `marlinPrinter.X_MAX`, `marlinPrinter.Y_MAX`, `marlinPrinter.Z_MAX`. |
|                         | **Scanner Parameters**              |             |
|                         | *Motor Speeds (Feedrate)*          | Determine speed of movement. Parameters are `VPDScanner.TRAVEL_FEEDRATE`, `VPDScanner.SCANNING_MOVE_FEEDRATE`, and `VPDScanner.EXTRUSION_MOTOR_FEEDRATE`. |
|                         | *Heights*                           | Parameters are `VPDScanner.SCAN_HEIGHT` and `VPDScanner.TRAVEL_HEIGHT`. |
|                         | *Cuevette Info*                     | Specifies deepest point syringe should reach in cuevette. Parameters are `CUEVETTE_X`, `CUEVETTE_Y`, and `CUEVETTE_Z`. |
|                         | *Wafer Variables*                   | Parameters related to wafer being scanned include `VPDScanner.WAFER_DIAM`, `VPDScanner.EDGE_GAP`, and `VPDScanner.DROPLET_DIAMETER`. |
|                         | *Scan Head Variables*               | Parameters related to physical scan head. Includes `SYRINGE_CAPACITY`, `SYRINGE_LENGTH`, `RACK_TEETH_PER_CM`, and `GEAR_TEETH`. |
| **Actions**             | scanner.loadSyringe() / scanner.unloadSyringe() | Manually load or unload syringe. |
|                         | scanner.doWaferScan()               | Scan area of specified wafer, center head, calculate and execute scan rings. |
|                         | scanner.useCuevette(dispense = TRUE/FALSE) | Use cuevette either as reservoir or sample holder based on `dispense` argument. |


## Instance Parameters
Instance paramaters **must** be provided when creating an instance of a class. The two classes in this project are *marlinPrinter* & *VPDScanner*. Each class has one parater that must be supplied when creating an instance.

While there is no technical reason for the separation of instance & class parameters, the separation between the two is meant to convey how often one should change the parameter. Instance parameters should be changed easily & freely without concern. Class paramaters should be changed more thoughtfully.

#### marlinPrinter: `filename`
- The filename argument must always be passed to a marlinPrinter. This filename is where the gcode commands will be written, always in the local directory. The name can either have *.gcode* or not, as there is handling in place for both cases.

#### VPDScanner: `sample_volume`
- This parameter tells the program how large of a droplet should be used to scan the wafer.

## Class Parameters
**NOTE: In order to change class parameters, the `changeDefaultParams(scanner)` function must be called at the start of the scan routine.**  
This separation was put in place to make the main function more concise & clear.

*All paramaters are in **mm** and **mL** unless otherwise specified.*

### --> Printer Parameters
#### *_OFFSET Parameters*
**Only modify these parameters if the physical printhead changes.** These parameters have been tuned for the given printhead and syringe.

The offset paramaters (`X_OFFSET`, `Y_OFFSET`, `Z_OFFSET`) tell the printer how far off the printehead is from the regular Ender 3 printhead. Thus, when the command to go to the center of the bed is written, the syringe nozzle actually goes to the center, instead of the old printhead being centered on the buildplate.

#### *_MAX Parameters*
The _MAX paramaters should be modified if the printer being used is not the Ender 3. These paramaters tell the program how large the printspace is, and this were the center of the print surface is.

`marlinPrinter.X_MAX`, `marlinPrinter.Y_MAX`, `marlinPrinter.Z_MAX`, all specify the maximum distance that can be travelled in one direction.

NOTE: The XY paramaters are not the usable printspace (which you may find searching online). Instead, they are the measured lengths of the buildplate. This is used so that the printhead centers itself on the center of the wafer.

### --> Scanner parameters

#### *Motor Speeds (Feedrate)*
This category includes:
- `VPDScanner.TRAVEL_FEEDRATE`
- `VPDScanner.SCANNING_MOVE_FEEDRATE`
- `VPDScanner.EXTRUSION_MOTOR_FEEDRATE`
    - **NOTE:** Be particularly careful modifying the extrusion motor feedrate, especially after changing the gears. The issue is specifically with too high feedrates, as they can chew up gears, damage the syringe, etc.

Feedrate measures how fast an axis should move, in units of mm/s. If you would like the axes to move faster, increase the value. To decrease speed, decrease the value. See above note for the extrusion motor feedrate.

### *Heights*
- `VPDScanner.SCAN_HEIGHT`
    - This value (in mm) changes the height of the syringe tip while scanning. If the drop is falling off or if the syringe is grinding into the wafer, this variable should be changed accordingly
- `VPDScanner.TRAVEL_HEIGHT`
    - Changes the height of the printhead when making large travel moves. **ENSURE that this height is high enough so that the printer will not run into the cuevette holder or any other obstructions.

### *Cuevette Info*
These three variables (`CUEVETTE_X`, `CUEVETTE_Y`, `CUEVETTE_Z`) specify the location of the deepest point the syringe head should reach in to the cuevette to load/unload samples.

### *Wafer Variables*
These variables specificy what wafer is being scanned and how to scan it.
- `VPDScanner.WAFER_DIAM`
    - The diameter of the wafer being scanned in mm.
- `VPDScanner.EDGE_GAP`
     - Since wafers have flats along the edges, the scanner does not scan the entire surface of the wafer, instead offsetting the first scan ring from the edge of the wafer. This parameter determines the length of that gap.
- `VPDScanner.DROPLET_DIAMETER`
    - The size of the scan drop on the wafer. By using the wafer diameter and edge gap, the program automatically calculates the amount of scan rings neccesary. Smaller drop diameter will mean there are more scan rings, vice versa.

### *Scan Head Variables*
In general these variables **should not** be changed unless the physical scan head is changed.

- `SYRINGE_CAPACITY` & `SYRINGE_LENGTH`
    - The capacity (mL) and length of that capacity (mm) of the syringe used. This allows the system to determine how far to move to dispense or collect a specific volume from the syringe.
- `RACK_TEETH_PER_CM` & `GEAR_TEETH`
    - Using the above syringe variables, the system can calculate the motor distance needed for specific volume extrusion moves. 

## Actions
In addition to changing *how* and *where* the scanner scans through parameters, you can also change *what* the scanner does during it's scan routine.

This sections the main actions that can be called during a VPD scanner's scan routine.

### scanner.loadSyringe() / scanner.unloadSyringe()
These routines allow you to manually load or unload the syringe before or after the scan routine as appropriate.

- `scanner.loadSyringe()`
    - This function moves the syringe to the origin and travel height, and opens the plunger holder to the appropriate height for the specified *sample_volume*.
    - **NOTE:** For this function to work properly, the plunger holder should be at the "0mL" mark on your syringe *before* starting the program. Since printers do not know nay absolute coordinates, and only know how to move relative to where they were, this function will move the plunger to the wrong location if the routine is not started at 0mL on the plunger holder.
- `scanner.unloadSyringe()`
    - Moves the printhead to the origin and travel height, opening the 

### scanner.doWaferScan()
This routine can be called to scan the appropriate area of any speified wafer. It will center the head, calculate the neccesary scan rings, and execute them. Then, it will collect the drop back up by doing a sweep backwards to pick up the tail of the drop.

### scanner.useCuevette(dispense = TRUE/FALSE)
This routine uses the cuevette as either a reservoir or sample holder depending on how the `dispense` argument is specified
- `dispense = TRUE`
    - This dispenses the collected droplet from the wafer into the cuevette.
- `dispense = FALSE`
    - Uses the cuevette as a fluid reservoir, withdrawing up `sample_volume` mL of fluid.