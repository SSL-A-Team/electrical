# Getting Started with A-Team Electrical

## Setting Up KiCAD

### Setting Up the KiCAD Library Path
- Click `Preferences->Configure Paths`
- Under `Environment Variables` click `+`
- Set the name `LIB_DIR_AT`
- Set the path to `<repository_location>/lib` where <repository_location> is the download location.

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

