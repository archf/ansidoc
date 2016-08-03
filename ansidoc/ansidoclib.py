import os
from jinja2 import Environment, PackageLoader
from . import helpers


class Ansidoc():
    """Main ansidoc Object."""

    def __init__(self, **kwargs):
        """initiate object with provided options."""
        self.dirpath = kwargs.get('dirpath')
        self.verbose = kwargs.get('verbose')
        self.dry_run = kwargs.get('dry_run')
        self.target = kwargs.get('target')

    def _make_role_symlink(self, rolepath):
        """
        Add symlink for each roles.

        since '../' cannot be use in a sphinx toctree, this will for a given
        role create a symlink from the <playbook_dir>/docs to
        <playbook_dir>/roles/rolename/docs/index.
        """
        # symlink src
        symlink_target = os.path.abspath(os.path.join(rolepath, self.target))

        # symlink dst
        symlink_name = "role-" + os.path.basename(rolepath) + "-" + self.target

        if self.verbose:
            print("Generating symlink to role " + symlink_target + " ...")

        if not os.path.islink(symlink_name):
            os.symlink(symlink_target, symlink_name)

    def _make_role_doc(self, rolepath):
        """
        Generate documentation on the fly for a single role.

        Informations are picked in defaults/main.yml and meta/main.yml.
        """
        role = os.path.basename(rolepath)

        print("Generating doc for role " + role + "...")
        if self.verbose:
            print("Current rolepath is : " + rolepath)

        # create symlink if needed
        if self.target:
            self._make_role_symlink(rolepath)

        # load meta/main.yml
        meta_file = os.path.join(rolepath, "meta/main.yml")
        if os.path.isfile(meta_file):
            metainfos = helpers.load_yml_file(meta_file)
            if self.verbose:
                print("Loaded role meta/main.yml: \n\n")
                print(metainfos)
                print("\n")
        else:
            metainfos = None
            if self.verbose:
                print(meta_file + " doesn't exist...")

        # load files in vars/*
        vars_files = helpers.read_files(
            os.path.join(rolepath, "vars"), self.verbose)

        # load defaults/*
        defaults_files = helpers.read_files(
            os.path.join(rolepath, "defaults"), self.verbose)

        # load template and create templating environment
        env = Environment(loader=PackageLoader('ansidoc', 'templates'),
                          lstrip_blocks=True,
                          trim_blocks=True)

        # render readme
        template = env.get_template('readme.j2')

        t = template.render(metainfos,
                            role_vars=vars_files,
                            role_defaults=defaults_files)

        if self.verbose or self.dry_run:
            print(t)

        # create readme file in rolepath/docs
        # makedirs(path.abspath(rolepath + "/docs"), mode=755, exist_ok=False)

        # create readme file in rolepath/README.md
        if not self.dry_run:
            helpers.write_file(t, os.path.join(rolepath, "README.md"))

        print("Role " + role + " ...done\n")

    def run(self):
        """
        Runner.

        Wrap the make_role_doc method to loop or not depending on
        the dirpath basename. See dirpath positional argument help for more
        details.
        """
        if os.path.basename(self.dirpath) == 'roles':
            # loop over multiple roles
            for role in os.listdir(self.dirpath):
                self._make_role_doc(os.path.join(self.dirpath, role))
        else:
            # run on a single role
            self._make_role_doc(self.dirpath)
