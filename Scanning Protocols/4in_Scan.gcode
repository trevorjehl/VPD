; BEGIN START GCODE
G21 ; set units to millimeters
M82 ;absolute extrusion mode
M302 S0; always allow extrusion (disable temp/length checking)
G92 E0 ; Reset Extruder
G28 ; Home all axes
G90 ; Set all axes to absolute
G92 E0 X0 Y0 Z0; Set home position
M92 E3938.5495 ; Set steps per unit.
M203 E6.0000 ; Set max E feedrate
G0 Z2.0000 F1250.0 ;Move up to prevent scratching.
;
; END START GCODE
;
G0 Z40.0000 F1250.0
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
M82; Set E to absolute positioning
G1 E0.2000 F6.0000 ; Open syringe holder.
M82; Set E to absolute positioning
G1 E0.0500 F6.0000 ; Open syringe holder.
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
G0 Z1.5000 F1250.0
G0 X149.5000 F2000.0000 ;Move to max radius
M82; Set E to absolute positioning
G1 E0.0000 F6.0000
G0 X149.5000 F80.0000 ;Move needle in.
G2 I-40.0000 J0.0000
G0 X146.5000 F80.0000 ;Move needle in.
G2 I-37.0000 J0.0000
G0 X143.5000 F80.0000 ;Move needle in.
G2 I-34.0000 J0.0000
G0 X140.5000 F80.0000 ;Move needle in.
G2 I-31.0000 J0.0000
G0 X137.5000 F80.0000 ;Move needle in.
G2 I-28.0000 J0.0000
G0 X134.5000 F80.0000 ;Move needle in.
G2 I-25.0000 J0.0000
G0 X131.5000 F80.0000 ;Move needle in.
G2 I-22.0000 J0.0000
G0 X128.5000 F80.0000 ;Move needle in.
G2 I-19.0000 J0.0000
G0 X125.5000 F80.0000 ;Move needle in.
G2 I-16.0000 J0.0000
G0 X122.5000 F80.0000 ;Move needle in.
G2 I-13.0000 J0.0000
G0 X119.5000 F80.0000 ;Move needle in.
G2 I-10.0000 J0.0000
G0 X116.5000 F80.0000 ;Move needle in.
G2 I-7.0000 J0.0000
G0 X113.5000 F80.0000 ;Move needle in.
G2 I-4.0000 J0.0000
G0 Z1.0000 F160.0000
G3 E1.0000 I-4.0000 J0.0000 X111.5000 Y134.9641 ; arc
G0 Z40.0000 F1250.0
G0 X109.5000 Y131.5000 F2000 ;CENTER HEAD
M82; Set E to absolute positioning
G1 E1.0000 F6.0000 ; Open syringe holder.
M400
M300 P200.0000 ; Beep.
M0 ; Stop and wait
M82; Set E to absolute positioning
G1 E0.0000 F6.0000 ; Close syringe holder so it is ready for the next cycle.
G91 ; Set all axes to relative
G0 Z15.0000 F1250.0 ;Raize Z.
G90 ; Set all axes to absolute
G0 X0.0000 Y235 F2000 ;Present print.
