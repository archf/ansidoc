from os import path, symlink
# , makedirs
# fixme: unable to import only safe_load
# from yaml import yaml.safe_load
import yaml
from jinja2 import Environment, PackageLoader

# import yaml2rst

# # def gen_toctree(title,text):
# #     toc = open("../roles/" + title + "/docs/index.rst",'w')
# #     toc.write(m2r("## " + title))
# #     toc.write(TOCTREE_TEMPLATE)
#         # generate a toctree for each roles
#         # gen_toctree(element, TOCTREE_TEMPLATE)


def _load_yml_file(filepath):
    """safe_load yaml file."""
    with open(filepath, 'r') as stream:
        return yaml.safe_load(stream)


def _write_file(data, filepath):
    """write a file to disk only if content has changed."""
    with open(filepath, 'r+') as f:
        # replace content only if needed
        if data != f.read():
            f.truncate(0)
            f.seek(0)
            f.write(data)

# def make_doc_dir():
#     """Create docs folder inside role."""
#     docdir = path.abspath(rolepath + "/docs")

#     # make sure destination exist, if not create it
#     if not path.isdir(symlink_target):
#         mkdir(symlink_target,'755')


def _make_role_doc_symlink(rolepath, target, verbose):
    """
    Add symlink for each roles.

    since '../' cannot be use in a sphinx toctree, this will for a given role
    create a symlink from the <playbook_dir>/docs to
    <playbook_dir>/roles/rolename/docs/index.
    """
    # symlink src
    symlink_target = path.abspath(path.join(rolepath, target))

    # symlink dst
    symlink_name = path.basename(rolepath) + "-role-" + target

    if verbose:
        print("Generating symlink to role " + symlink_target + " ...")

    if not path.islink(symlink_name):
        symlink(symlink_target, symlink_name)


def make_role_doc(rolepath, **kwargs):
    """
    Generate documentation on the fly for a single role.

    Informations are picked in defaults/main.yml and meta/main.yml.
    """
    verbose = kwargs.get('verbose')
    dry_run = kwargs.get('dry_run')
    target = kwargs.get('target')

    if target:
        _make_role_doc_symlink(rolepath, target, verbose)

    if verbose:
        print(rolepath)
        print("Generating doc for role " + path.basename(rolepath) + "...")

    # load defaults/main.yml file
    if path.isfile(rolepath + "/defaults/main.yml"):
        with open(rolepath + "/defaults/main.yml", 'r') as f:
            # fixme: "skip ---\n in a better way"
            f.seek(5)
            default_vars = f.read()
    else:
        default_vars = None
        if verbose:
            print(rolepath + "/defaults/main.yml doesn't exist...")

    # load meta/main.yml
    if path.isfile(rolepath + "/meta/main.yml"):
        metainfo = _load_yml_file(rolepath + "/meta/main.yml")
        print(metainfo)
    else:
        metainfo = None
        if verbose:
            print(rolepath + "/meta/main.yml doesn't exist...")

    # load template and create templating environment
    env = Environment(loader=PackageLoader('ansidoc', 'templates'),
                      lstrip_blocks=True,
                      trim_blocks='true')

    # env = Environment(loader=FileSystemLoader('ansidoclib'),
    #                   lstrip_blocks='true',
    #                   trim_blocks='true')

    # render readme
    template = env.get_template('readme.j2')

    t = template.render(metainfo, role_default_vars=default_vars)

    if verbose and (default_vars is not None and metainfo is not None):
        print(t)

    # makedirs(path.abspath(rolepath + "/docs"), mode=755, exist_ok=False)

    # create file in rolepath/docs and rolepath/README.md
    if not dry_run and (default_vars is not None and metainfo is not None):
        _write_file(t, path.join(rolepath, "README.md"))
