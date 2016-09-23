# Ansidoc

ansidoc is a simple tool to generate your ansible role documentation.

# Usage

## Prepare your role

For best results, create a `docs/docs.yml` file inside your role and fill those
variables:

```yaml
---

github_account: <your-role-github-account-username>
todos: [] # (optional) list of todos to print in your README file
requirements: [] # (optional) explanation of requirements to use your role

# some details so people know what your role does.
description: |
  This role will do blablabla...
  - install packages
  - add a few mounts
  - configure a daemon
  - ...
```

Content of your role `vars/*` and `defaults/*` will also be literally inserted
in between `yaml` codeblocks. Put nice comments//explanations in them!

## cli

```shell
usage: __main__.py [-h] [-v] [-V] [-d] [-s TARGET] dirpath

positional arguments:
  dirpath        Either a roles_path wich is a roles' directory or a path to a single role. If roles_path basename is
                 'roles' it will loop over subdirectories assuming each of them contains a role.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
  -V, --version  show program's version number and exit
  -d, --dry-run  dry run
  -s TARGET      (docs | README.md ) Create a symlink in PWD to TARGET. This is usefull when used from sphinx as you
                 cannot add relative entries such as '../*' in the toctree. If unspecified, no symlink is created
```

## From sphinx

You can import in your code and pass arguments similarly as you would do on the
cli.

For example:

```python
from ansidoc import Ansidoc
ansidoc = Ansidoc(dirpath=<path/to/role>, dry_run=True)
ansidoc.run()
```

# wishlist

- role dependency grapher
- role variables analysis (to audit what is defined where)
- create sphinx documentation for this program
- make this a sphinx plugin

# License

MIT.
