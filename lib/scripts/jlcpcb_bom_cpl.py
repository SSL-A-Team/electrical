#
# BoM & CPL Generator for JLCPCB PCBA
#

"""
    @package
    Output: CSV (comma-separated)
    Grouped By: Value, Footprint
    Sorted By: Ref
    BoM Fields: Comment, Designator, Footprint
    CPL Fields: Designator, Mid X, Mid Y, Layer, Rotation

    Command line:
    python "pathToFile/jlcpcb_bom_cpl.py" "%I" "%O"
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import kicad_utils
import csv
import sys

# A helper function to filter/convert a string read in netlist
# currently: do nothing


def fromNetlistText(aText):
    return aText


# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead

project_name = sys.argv[2]
bom_name = project_name + '-bom.csv'
cpl_name = project_name + '-cpl.csv'

try:
    f = kicad_utils.open_file_writeUTF8(bom_name, 'w')
except IOError:
    e = "Can't open output file for writing: " + bom_name
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=',',
                 quotechar='\"', quoting=csv.QUOTE_ALL)

# Output header row
out.writerow(['Comment', 'Designator', 'Footprint'])


# Get all of the components in groups of matching parts + values
# (see ky_generic_netlist_reader.py)
grouped = net.groupComponents()

# Output all of the component information
for group in grouped:
    refs = ""

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        refs += fromNetlistText(component.getRef()) + ", "
        c = component
    out.writerow([
        fromNetlistText(c.getValue()),
        refs[:-2],
        fromNetlistText(c.getFootprint())
    ])
