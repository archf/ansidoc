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
        self.dirpath = os.path.expanduser(kwargs.get('dirpath'))
        self.opts = kwargs

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

        if self.verbose:
            print("Generating doc for role '%s'..." % rolename)
            print("Current rolepath is: '%s'" % rolepath)

        # create symlink if needed
        if self.target:
            self._make_role_symlink(rolepath)

        # load role meta/main.yml
        meta_vars = helpers.load_yml_file(
            os.path.join(rolepath, "meta/main.yml"), self.verbose)

        # load role docs/*.yml
        docs_vars = helpers.load_yml_files(
            os.path.join(rolepath, "docs"), self.verbose)

        # load literaly role docs/*.md
        docs_md_files = helpers.read_files(
            os.path.join(rolepath, "docs"), '*.md', self.verbose)

        # load literaly role vars/*.yml
        vars_files = helpers.read_files(
            os.path.join(rolepath, "vars"), '*.yml', self.verbose)

        # load literaly role defaults/*.yml
        defaults_files = helpers.read_files(
            os.path.join(rolepath, "defaults"), '*.yml', self.verbose)

        # load template and create templating environment
        env = Environment(loader=PackageLoader('ansidoc', 'templates'),
                          lstrip_blocks=False, trim_blocks=True)

        # render readme
        template = env.get_template('readme.j2')

        # render method accepts the same arguments as the dict constructor
        t = template.render(self.opts,
                            rolename=rolename,
                            role_meta_vars=meta_vars,
                            role_docs_vars=docs_vars,
                            role_docs_md_files=docs_md_files,
                            role_vars_files=vars_files,
                            role_defaults_files=defaults_files
                            )

        if self.verbose or self.dry_run:
            print(t)

        # create readme file in rolepath/README.md
        if not self.dry_run:
            helpers.write_file(t, os.path.join(rolepath, "README.md"))

        if self.verbose:
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
