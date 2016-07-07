# Ansidoc

ansidoc is a simple tool to generate your ansible role documentation

# Usage

### cli

```shell

usage: ansidoc [-h] [-v] [-V] [-o OUT_FILE] path

positional arguments:
  path                  search path, either roles_path wich is a roles dir or a path to a single roles. If roles_path basename is 'roles', it will loop over subdirectories assuming each of them contains a roles

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -V                    show program's version number and exit
  -o OUT_FILE, -w OUT_FILE
                        output file path (export and config subcommands)

# todo
  - implement outfile behavior
  - implement program version
  -
```

### from sphinx

```python

import ansidoc

```

# wishlist

- role dependency grapher
- role variables analysis (to audit what is defined where)

# License

Mit.
