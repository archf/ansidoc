# Ansidoc

ansidoc is a simple tool to generate your ansible role documentation

# Usage

### cli

```shell
usage: ansidoc [-h] [-v] [-V] [-d] [-s TARGET] dirpath

positional arguments:
  dirpath        Either a roles_path wich is a roles' directory or a path to a single role. If roles_path basename is
                 'roles' it will loop over subdirectories assuming each of them contains a role.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
  -V, --version  show program's version number and exit
  -d             dry run
  -s TARGET      (docs | README.md ) Create a symlink from PWD to TARGET. This is usefull when used from sphinx as
                 you cannot add relative entries such as '../*' in the toctree.
```

### From sphinx

You can import in your code and pass arguments similarly as you would do on the
cli.

For example:

```python
from ansidoc import ansidocgen
ansidocgen(dirpath=<path/to/role>, dry_run=True)
```

# wishlist

- role dependency grapher
- role variables analysis (to audit what is defined where)
- create sphinx documentation for this program

# License

Mit.
