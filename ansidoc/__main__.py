#!/usr/bin/env python3

import argparse
from os import path
import ansidoc


def get_version(prog):
    """
    Retreive software version
    """
    print(prog + 'from callback')
    from ansidoc import __version__
    return __version__.__version__


def main():

    PACKAGE_DIR = path.abspath(__file__)
    print(PACKAGE_DIR)

    # create parser objects
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    parser.add_argument('-V', action='version',
                        version='%(prog)s ' + get_version('%(prog)s'))

    parser.add_argument("-o", "-w", dest="out_file",
                        help="output file path (export and config subcommands)")

    parser.add_argument("path", help="search path, either roles_path wich is a \
                        roles dir or a path to a single roles. If roles_path \
                        basename is 'roles', it will loop over subdirectories \
                        assuming each of them contains a roles")

    args = parser.parse_args()
    ansidoc(args)

if __name__ == "__main__":
    main()
