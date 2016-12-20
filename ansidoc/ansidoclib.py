import os
from jinja2 import Environment, PackageLoader
from . import helpers


class Ansidoc():
    """Main ansidoc Object."""

    def __init__(self, **kwargs):
        """initiate object with provided options."""
        self.verbose = kwargs.get('verbose')
        self.dry_run = kwargs.get('dry_run')
        self.target = kwargs.get('target')
        self.dirpath = kwargs.get('dirpath')

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
            print("Generating symlink to role '%s' ..." % symlink_target)

        if not os.path.islink(symlink_name):
            os.symlink(symlink_target, symlink_name)

    def _make_role_doc(self, rolepath):
        """
        Generate documentation for a single role.

        Informations are picked in defaults/*, vars/* meta/main.yml and
        docs/*.yml.
        """

        rolename = os.path.basename(os.path.abspath(rolepath))

        print("Generating doc for role '%s'..." % rolename)
        if self.verbose:
            print("Current rolepath is: '%s'" % rolepath)

        # create symlink if needed
        if self.target:
            self._make_role_symlink(rolepath)

        # load meta/main.yml
        metainfos = helpers.load_yml_file(
            os.path.join(rolepath, "meta/main.yml"), self.verbose)

        # load docs/main.yml
        docfile = helpers.load_yml_file(
            os.path.join(rolepath, "docs/docs.yml"), self.verbose)

        # load files in vars/*
        vars_files = helpers.read_files(
            os.path.join(rolepath, "vars"), self.verbose)

        # load defaults/*
        defaults_files = helpers.read_files(
            os.path.join(rolepath, "defaults"), self.verbose)

        # load template and create templating environment
        env = Environment(loader=PackageLoader('ansidoc', 'templates'),
                          lstrip_blocks=True, trim_blocks=True)

        # render readme
        template = env.get_template('readme.j2')

        # render method accepts the same arguments as the dict constructor
        t = template.render(metainfos,
                            rolename=rolename,
                            role_doc=docfile,
                            role_vars=vars_files,
                            role_defaults=defaults_files)

        if self.verbose or self.dry_run:
            print(t)

        # create readme file in rolepath/README.md
        if not self.dry_run:
            helpers.write_file(t, os.path.join(rolepath, "README.md"))

        print("Role '%s' ...done\n" % rolename)

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
