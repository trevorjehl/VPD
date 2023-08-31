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
G0 X174.5000 F2000.0000 ;Move to max radius
M82; Set E to absolute positioning
G1 E0.0000 F6.0000
G0 X174.5000 F80.0000 ;Move needle in.
G2 I-65.0000 J0.0000
G0 X171.5000 F80.0000 ;Move needle in.
G2 I-62.0000 J0.0000
G0 X168.5000 F80.0000 ;Move needle in.
G2 I-59.0000 J0.0000
G0 X165.5000 F80.0000 ;Move needle in.
G2 I-56.0000 J0.0000
G0 X162.5000 F80.0000 ;Move needle in.
G2 I-53.0000 J0.0000
G0 X159.5000 F80.0000 ;Move needle in.
G2 I-50.0000 J0.0000
G0 X156.5000 F80.0000 ;Move needle in.
G2 I-47.0000 J0.0000
G0 X153.5000 F80.0000 ;Move needle in.
G2 I-44.0000 J0.0000
G0 X150.5000 F80.0000 ;Move needle in.
G2 I-41.0000 J0.0000
G0 X147.5000 F80.0000 ;Move needle in.
G2 I-38.0000 J0.0000
G0 X144.5000 F80.0000 ;Move needle in.
G2 I-35.0000 J0.0000
G0 X141.5000 F80.0000 ;Move needle in.
G2 I-32.0000 J0.0000
G0 X138.5000 F80.0000 ;Move needle in.
G2 I-29.0000 J0.0000
G0 X135.5000 F80.0000 ;Move needle in.
G2 I-26.0000 J0.0000
G0 X132.5000 F80.0000 ;Move needle in.
G2 I-23.0000 J0.0000
G0 X129.5000 F80.0000 ;Move needle in.
G2 I-20.0000 J0.0000
G0 X126.5000 F80.0000 ;Move needle in.
G2 I-17.0000 J0.0000
G0 X123.5000 F80.0000 ;Move needle in.
G2 I-14.0000 J0.0000
G0 X120.5000 F80.0000 ;Move needle in.
G2 I-11.0000 J0.0000
G0 X117.5000 F80.0000 ;Move needle in.
G2 I-8.0000 J0.0000
G0 X114.5000 F80.0000 ;Move needle in.
G2 I-5.0000 J0.0000
G0 Z1.0000 F160.0000
G3 E1.0000 I-5.0000 J0.0000 X112.0000 Y135.8301 ; arc
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
