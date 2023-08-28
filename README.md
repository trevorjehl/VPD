[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Static Badge](https://img.shields.io/badge/PRs-Welcome-green)

# Low-Cost Open Source Vapor Phase Decomposition Scanner

This purpose of this project is to create a low-cost vapor phase decomposition droplet scanner for use in semiconductor research labs. Although traditional semiconductor manufactureres have access to the large, expensive VPD machines to evaluate silicon wafer contamination, these machines can be innacesible for smaller research facilities.

This project uses a modififed low-cost, open source 3D-printer as the basic platform for the scanner. A custom printehead was designed to hold a 1mL acid-resistant (polypropylene) plastic syringe. This repo contains the neccesary code to program complex scanning sequences for the scanning apparatus.

## Download & Installation

To download the project, copy all project files to your hard drive. This can be done either by downloading the project, cloning the repo, or creating a branch.

- This project runs on Python 3.1, so ensure your Python installation is up to date.
- The only dependency for this project is the `math` module.

## Command Line Usage
To create a new G-Code file, use the following command line syntax:
```console
foo@bar:~$ python3 GCodeCaller.py filename.gcode
```
This will create a *.gcode* file in your local directory according to the settings and steps outlined in GCodeCaller.py.

## Modifying The Scan Routine
Refer to [CUSTOM_SCAN.md](CUSTOM_SCAN.md). This includes various wafer sizes, using cuevettes for dispensing/collecting fluid, changing the location of the cuevette, scan speed, etc.

This project was created with customization in mind.

## Credits
This project was made in collaboration with Uriel Valencia. Overseen by [Alexander Denton](https://profiles.stanford.edu/alexander-denton), Stanford Nanofabrication Facility.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

For further details, see <https://www.gnu.org/licenses/>.