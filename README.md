[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Static Badge](https://img.shields.io/badge/PRs-Welcome-green)
![Static Badge](https://img.shields.io/badge/Python_Style-Black-black)

![Stanford](/Guides%20&%20Additional%20Documentation/Assets/StanfordLogo.png) ![SNF](/Guides%20&%20Additional%20Documentation/Assets/SNF.png)

# Low-Cost Open Source Vapor Phase Decomposition Scanner

This purpose of this project is to create a low-cost vapor phase decomposition droplet scanner for use in semiconductor research labs. 

![Scanner_Running_gif](/Guides%20&%20Additional%20Documentation/Assets/scannerRunning.gif)

<!-- ## Table of Contents

| Sections      | Description  |
|---------------|--------------|
| [Introduction](#introduction) | - Low-Cost Open Source Vapor Phase Decomposition Scanner<br> - Project Purpose |
| [Rationale](#rationale) | |
| [Download & Installation](#download--installation) | - Download Methods<br> - Python Version<br> - Project Dependencies |
| [Command Line Usage](#command-line-usage) | - Generating G-Code Files<br> - Usage on Ender 3 3D Printer |
| [Modifying The Scan Routine](#modifying-the-scan-routine) | - Custom Scan Documentation<br> - Advanced Modifications<br> - Contribution Guidelines |
| [Project Goals & Next Steps](#project-goals--next-steps) | - Scan Base Redesign<br> - Wafer Piece Scanning<br> - Increasing Scan Droplet Volume<br> - Enclosure Design<br> - Construction & Replication Instructions |
| [Credits](#credits) | - Collaborators<br> - Supervision |
| [License](#license) | - GPL v3 Licensing Information | -->


## Rationale

Although traditional semiconductor manufactureres have access to the large, expensive VPD machines to evaluate silicon wafer contamination, these machines can be innacesible for smaller research facilities.

This project uses a modififed low-cost, open source 3D-printer as the basic platform for the scanner. A custom printehead was designed to hold a 1mL acid-resistant (polypropylene) plastic syringe. This repo contains the neccesary code to program complex scanning sequences for the scanning apparatus.

## Download & Installation

To download the project, copy all project files to your hard drive. This can be done either by downloading the project, cloning the repo, or creating a branch.

- This project runs on Python 3.11.4, so ensure your Python installation is up to date.
- The only dependency for this project is the `math` module.

## Command Line Usage
To create a new G-Code file, use the following command line syntax:

```console
foo@bar:~$ python3 TEMPLATE.py filename.gcode
```

This will create a `.gcode` file in your local directory according to the settings and steps outlined in TEMPLATE.py. To run this easily on the Ender 3 3D printer (or similar), two methods can be used. For testing, software such as Repetier Host can be used, which communicates with 3D Printers over USB.

For more permanent installation, the `.gcode` file can be copied over to the 3D printer's SD/microSD card, which can then be run using the 3D printer's interface

## Modifying The Scan Routine
Refer to [CUSTOM_SCAN.md](/Guides%20&%20Additional%20Documentation/CUSTOM_SCAN.md) for detailed documentation, including various wafer sizes, using cuevettes for dispensing/collecting fluid, changing the location of the cuevette, scan speed, etc.

This project was created with customization in mind, and is therefore easy to modify to suit your needs. For more in-depth changes, consult [USING_TEMPLATE.md](/Guides%20&%20Additional%20Documentation/USING_TEMPLATE.md). 

If you do make changes, please contribute per the standards outlined in [CONTRIBUTING.md](CONTRIBUTING.md). As a reminder, if you release the modified version to the public in some way, the GNU license agreement requires you to make the modified source code available to the program's users.


## Project Goals & Next Steps
- [ ] Complete redesign of scan base to be CNC machined from Teflon/PTFE
- [ ] Add wafer piece scanning functionality (vacuum chuck?).
- [ ] Consider methods of increasing scan droplet volume, as this may aid ICP-MS measurements.
- [ ] Design encolosure/spill area to contain the system and any acid that may spill during operation.
- [ ] Create detailed construction/replication instructions with photos for use in other fabs.

## Credits
This project was made in collaboration with Uriel Valencia. Overseen by [Alexander Denton](https://profiles.stanford.edu/alexander-denton), Stanford Nanofabrication Facility. 

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

For further details, see <https://www.gnu.org/licenses/>.