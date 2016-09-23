"""Module main entry point."""

import sys
import argparse
from . import cli


def get_version(package):
    """Retreive software version."""
    from . import __version__
    return __version__.__version__ + "\nPython " + sys.version


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()

    # mostly always needed options
    parser.add_argument("-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    parser.add_argument('-V',
                        '--version',
                        action='version',
                        version='%(prog)s ' + get_version('%(prog)s'))

    # further customize the parser object
    cli._augment_parser(parser)
    args = parser.parse_args()

    exit_code = cli.run(**vars(args))
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
