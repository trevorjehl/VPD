; BEGIN START GCODE
G21 ; set units to millimeters
M82 ;absolute extrusion mode
M302 S0; always allow extrusion (disable checking)
G92 E0 ; Reset Extruder
G28 ; Home all axes
G90; Absolute positioning
G92 E0 X0 Y0 Z0; Set home position
M203 E1500
G1 Z2.0; Move up to prevent scratching
; END START GCODE
G0 Z3.0000 ;BEGIN CENTER HEAD
G0 X110.0000 Y110.0000
G0 Z1.0000 ;END CENTER HEAD
G0 Z3.0000
G0 X155.8000 F1500.0000 ;Move needle in.
G2 I-45.8000 J0.0000
G0 X154.8000 F1500.0000 ;Move needle in.
G2 I-44.8000 J0.0000
G0 X153.8000 F1500.0000 ;Move needle in.
G2 I-43.8000 J0.0000
G0 X152.8000 F1500.0000 ;Move needle in.
G2 I-42.8000 J0.0000
G0 X151.8000 F1500.0000 ;Move needle in.
G2 I-41.8000 J0.0000
G0 X150.8000 F1500.0000 ;Move needle in.
G2 I-40.8000 J0.0000
G0 X149.8000 F1500.0000 ;Move needle in.
G2 I-39.8000 J0.0000
G0 X148.8000 F1500.0000 ;Move needle in.
G2 I-38.8000 J0.0000
G0 X147.8000 F1500.0000 ;Move needle in.
G2 I-37.8000 J0.0000
G0 X146.8000 F1500.0000 ;Move needle in.
G2 I-36.8000 J0.0000
G0 X145.8000 F1500.0000 ;Move needle in.
G2 I-35.8000 J0.0000
G0 X144.8000 F1500.0000 ;Move needle in.
G2 I-34.8000 J0.0000
G0 X143.8000 F1500.0000 ;Move needle in.
G2 I-33.8000 J0.0000
G0 X142.8000 F1500.0000 ;Move needle in.
G2 I-32.8000 J0.0000
G0 X141.8000 F1500.0000 ;Move needle in.
G2 I-31.8000 J0.0000
G0 X140.8000 F1500.0000 ;Move needle in.
G2 I-30.8000 J0.0000
G0 X139.8000 F1500.0000 ;Move needle in.
G2 I-29.8000 J0.0000
G0 X138.8000 F1500.0000 ;Move needle in.
G2 I-28.8000 J0.0000
G0 X137.8000 F1500.0000 ;Move needle in.
G2 I-27.8000 J0.0000
G0 X136.8000 F1500.0000 ;Move needle in.
G2 I-26.8000 J0.0000
G0 X135.8000 F1500.0000 ;Move needle in.
G2 I-25.8000 J0.0000
G0 X134.8000 F1500.0000 ;Move needle in.
G2 I-24.8000 J0.0000
G0 X133.8000 F1500.0000 ;Move needle in.
G2 I-23.8000 J0.0000
G0 X132.8000 F1500.0000 ;Move needle in.
G2 I-22.8000 J0.0000
G0 X131.8000 F1500.0000 ;Move needle in.
G2 I-21.8000 J0.0000
G0 X130.8000 F1500.0000 ;Move needle in.
G2 I-20.8000 J0.0000
G0 X129.8000 F1500.0000 ;Move needle in.
G2 I-19.8000 J0.0000
G0 X128.8000 F1500.0000 ;Move needle in.
G2 I-18.8000 J0.0000
G0 X127.8000 F1500.0000 ;Move needle in.
G2 I-17.8000 J0.0000
G0 X126.8000 F1500.0000 ;Move needle in.
G2 I-16.8000 J0.0000
G0 X125.8000 F1500.0000 ;Move needle in.
G2 I-15.8000 J0.0000
G0 X124.8000 F1500.0000 ;Move needle in.
G2 I-14.8000 J0.0000
G0 X123.8000 F1500.0000 ;Move needle in.
G2 I-13.8000 J0.0000
G0 X122.8000 F1500.0000 ;Move needle in.
G2 I-12.8000 J0.0000
G0 X121.8000 F1500.0000 ;Move needle in.
G2 I-11.8000 J0.0000
G0 X120.8000 F1500.0000 ;Move needle in.
G2 I-10.8000 J0.0000
G0 X119.8000 F1500.0000 ;Move needle in.
G2 I-9.8000 J0.0000
G0 X118.8000 F1500.0000 ;Move needle in.
G2 I-8.8000 J0.0000
G0 X117.8000 F1500.0000 ;Move needle in.
G2 I-7.8000 J0.0000
G0 X116.8000 F1500.0000 ;Move needle in.
G2 I-6.8000 J0.0000
G0 X115.8000 F1500.0000 ;Move needle in.
G2 I-5.8000 J0.0000
G0 X114.8000 F1500.0000 ;Move needle in.
G2 I-4.8000 J0.0000
G0 X113.8000 F1500.0000 ;Move needle in.
G2 I-3.8000 J0.0000
G0 X112.8000 F1500.0000 ;Move needle in.
G2 I-2.8000 J0.0000
G0 X111.8000 F1500.0000 ;Move needle in.
G2 I-1.8000 J0.0000
G91 ; Set all axes to relative
G0 Z10.0000 ;Raize Z.
G90 ; Set all axes to absolute
G0 X0.0000 Y220.0000 ;Present print.