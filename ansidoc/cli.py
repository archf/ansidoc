"""Enhance parser object and run commands."""
from os import path, listdir

from .ansidoclib import make_role_doc


def _augment_parser(parser):
    """Augment parser object with more args."""
    # parser.add_argument(
    #     "-o",
    #     "-w",
    #     dest="out_file",
    #     help="output file path (export and config subcommands)")

    parser.add_argument("-d", "--dry-run", action='store_true', dest="dry_run",
                        help="dry run")

    parser.add_argument(
        "-s",
        dest="target",
        help="(docs | README.md ) Create a symlink in PWD to TARGET. This is \
            usefull when used from sphinx as you cannot add relative entries \
            such as '../*' in the toctree. If unspecified, no symlink is \
            created")

    parser.add_argument(
        "dirpath",
        help="Either a roles_path wich is a roles' directory or a path to a \
            single role. If roles_path basename is 'roles' it will loop over \
            subdirectories assuming each of them contains a role.")


def run(**kwargs):
    """
    Runner.

    Calls the make_role_doc function within a loop or not depending on
    the dirpath basename. See dirpath positional argument help for more
    details.
    """
    dirpath = kwargs.get('dirpath')

    if path.basename(dirpath) == 'roles':
        # loop over multiple roles
        for role in listdir(dirpath):
            make_role_doc(path.join(dirpath, role), **kwargs)
    else:
        # run on a single role
        make_role_doc(dirpath, **kwargs)
