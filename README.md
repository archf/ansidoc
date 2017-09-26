# Ansidoc

A simple tool to generate ansible role's documentation.

## Usage

This tool generates a `README.md` file using data from multiple sources.

* From role content:
  * role `defaults/main.yml`
  * role `vars/*.yml`
* You content.
  * role `docs/*.yml`
  * role `docs/*.md`

Content of your role `vars/*` and `defaults/*` will also be literally inserted
in between `yaml` codeblocks. Put nice comments//explanations of variable's
purpose in them!

The role `docs` directory may contain YAML files that will be parsed. Variables
within will be use to enrich the resulting `README.md` file. All markdown files
will also be include. Top header must be of level H2. Currently there are no
mechanism to defined the inclusion order.

### Prepare your role

For best results, create a `docs/<you-var-file>.yml` file inside your role and fill those
variables:

```yaml
---

github_account: <your-role-github-account-username>
todos: [] # (optional) list of todos to print in your README file
```

### cli

```shell
usage: ansidoc [-h] [-v] [-V] [-d] [-s TARGET] [-nf] [-e EXCLUDE] [-p] dirpath

positional arguments:
  dirpath               Either a 'roles_path' wich is a roles' directory or a
                        path to a single role. If 'roles_path' basename is
                        'roles' it will loop over subdirectories assuming each
                        of them contains a role.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -V, --version         show program's version number and exit
  -d, --dry-run         dry run, Outputs pure markdown to stdout nothing is
                        written to disk
  -s TARGET             (docs | README.md) Create a symlink in PWD to TARGET.
                        This is useful when used from sphinx as you cannot add
                        relative entries such as '../*' in the toctree. If
                        unspecified, no symlink is created.
  -nf, --no-ansidoc-footer
                        Do not render the ansidoc project footer.
  -e EXCLUDE, --exclude EXCLUDE
                        csv list of role names to exclude. Must match
                        directory name found under specified 'dirpath'
  -p, --private         Consider role(s) private, e.g.: Skip installation from
                        github part from rendered template.
```

### From sphinx

You can import in your code and pass arguments similarly as you would do on the
cli.

For example:

```python
from ansidoc import Ansidoc
ansidoc = Ansidoc(dirpath=<path/to/role>, dry_run=True)
ansidoc.run()
```

## wishlist

- role dependency grapher
- role variables analysis (to audit what is defined where)
- create sphinx documentation for this program
- make this a sphinx plugin
- include mardown files in defined order (alphabetical?, number the files?)
- override parts of template with custom one.
  - search paths to find templates (`.ansidoc/templates/*`?)
- multi-role variables
  - search paths to find config (`.ansidoc/config.yml`?)
  - exclude list configurable in config file

## License

MIT.

## Similar Projects

* [Ansible-DocGen](https://github.com/toast38coza/Ansible-DocGen)
