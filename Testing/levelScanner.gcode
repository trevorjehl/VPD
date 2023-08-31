; BEGIN START GCODE
G21 ; set units to millimeters
M82 ;absolute extrusion mode
M302 S0; always allow extrusion (disable temp/length checking)
G92 E0 ; Reset Extruder
G28 ; Home all axes
G90 ; Set all axes to absolute
G92 E0 X0 Y0 Z0; Set home position
M92 E3938.5495 ; Set steps per unit.
M203 E10.0000 ; Set max E feedrate
G0 Z2.0000 F1250.0 ;Move up to prevent scratching.
;
; END START GCODE
;
G0 Z40.0000 F1250.0
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
M82; Set E to absolute positioning
G1 E0.2000 F10.0000 ; Open syringe holder.
M82; Set E to absolute positioning
G1 E0.0000 F10.0000 ; Open syringe holder.
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G0 Z0.0000 F500.0000
G91 ; Set all axes to relative
G0 X32.5269 Y32.5269 F500 
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G90 ; Set all axes to absolute
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G91 ; Set all axes to relative
G0 X32.5269 Y-32.5269 F500 
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G90 ; Set all axes to absolute
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G91 ; Set all axes to relative
G0 X-32.5269 Y32.5269 F500 
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G90 ; Set all axes to absolute
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G91 ; Set all axes to relative
G0 X-32.5269 Y-32.5269 F500 
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G90 ; Set all axes to absolute
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G91 ; Set all axes to relative
G0 X32.5269 Y32.5269 F500 
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G90 ; Set all axes to absolute
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G91 ; Set all axes to relative
G0 X32.5269 Y-32.5269 F500 
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G90 ; Set all axes to absolute
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G91 ; Set all axes to relative
G0 X-32.5269 Y32.5269 F500 
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G90 ; Set all axes to absolute
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G91 ; Set all axes to relative
G0 X-32.5269 Y-32.5269 F500 
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G90 ; Set all axes to absolute
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G0 Z40.0000 F1250.0
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
M82; Set E to absolute positioning
G1 E1.0000 F10.0000 ; Open syringe holder.
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
M82; Set E to absolute positioning
G1 E0.0000 F10.0000 ; Close syringe holder so it is ready for the next cycle.
G91 ; Set all axes to relative
G0 Z15.0000 F1250.0 ;Raize Z.
G90 ; Set all axes to absolute
G0 X0.0000 Y235 F2000 ;Present print.
