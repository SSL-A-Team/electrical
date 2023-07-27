# Getting Started with A-Team Electrical

All current board releases use KiCad 7.X. 

See [releases](https://github.com/SSL-A-Team/electrical/releases) for competition production files. Our releases include known bug documentation, and the confirmed gerber, BoM, and CPL files sent to fab so you know you're looking and ordering what we did. Releases are accompanied by a tagged commit, for all editable project files used to generate the fab products.

For complex boards like control and kicker, we include spice models and python files that compute any relevant values from datasheets, and including documented references and links to needed formulations. 

## Setting Up KiCAD

### Setting Up the KiCAD Library Path
- Click `Preferences->Configure Paths`
- Under `Environment Variables` click `+`
- Set the name `LIB_DIR_AT`
- Set the path to `<repository_location>/lib` where \<repository_location\> is the download location.

Example entry:
- Name: `LIB_DIR_AT`
- Path: `C:\Users\guyfl\Documents\A-Team\electrical\lib`

### Setting Up JLCPCB Plugin

KiCAD version 6.99 (nightly) or newer should install the [KiCAD JLCPCB Tools](https://github.com/Bouni/kicad-jlcpcb-tools) plugin. 

## Setting Up the Python Environment
 1. We recommend creating a python environment using `python3 -m venv venv` (python 10 appears to be required)
 2. Install poetry `pip install poetry`
 3. Run any python file with `poetry run python <python_file>`
 4. (Optional) Add dependencies with `poetry add <dependency>`

## Soldering

Our [soldering process](SOLDERING.md) is documented. Advanced components like modern SMPS chips and current sense motor hardware proved sensitive to technique. The team's tries to PCBA as much as possible, but sometime it's too expensive to PCBA all chips, especially advanced ones not in stock at the fab house. 
