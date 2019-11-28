#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


def read_profile(infile):
    """
    Reads contents of an airfoil definition file such as the
    ones found here:
    http://m-selig.ae.illinois.edu/ads/coord_database.html
    
    Many have an airfoil name, followed by 2 values
    indicating number of points for upper and lower surface,
    then a list of upper surface points and finally the lower
    surface points.
    
    """
    # Skips airfoil name
    name = infile.readline()

    # Read the points, then skip any blank lines
    raw = [[float(c) for c in line.split()] for line in infile]
    raw = [(p[0], p[1]) for p in raw if len(p) == 2]

    # The first pair may be the length of the upper and lower data
    len_upper = int(raw[0][0])
    len_lower = int(raw[0][1])
    if len_upper > 1 or len_lower > 1:
        raw = raw[1:]
        coordinates = raw[len_upper-1::-1]
        coordinates.extend(raw[len_upper+1:]) #skip the repeated (0,0)
    else:
        coordinates = raw

    return name, coordinates


def main():
    """ Main entry point of the app """
    with open("examples\clarky.txt") as f:
        name, coordinates = read_profile(f)

    print(name)
    for c in coordinates:
        print(c)

    print(len(coordinates))

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()