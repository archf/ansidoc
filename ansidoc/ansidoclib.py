import os
import fnmatch
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


def _load_yml_file(fpath):
    """safe_load yaml file."""
    with open(fpath, 'r') as stream:
        return yaml.safe_load(stream)


def _write_file(data, fpath):
    """write a file to disk only if content has changed."""
    if not os.path.isfile(fpath):
        with open(fpath, 'w') as f:
            f.write(data)
    else:
        with open(fpath, 'r+') as f:
            # replace content only if needed
            if data != f.read():
                f.truncate(0)
                f.seek(0)
                f.write(data)


def _get_filenames(dpath):
    """Return *.{yml,json} files in given directory."""
    for file in os.listdir(dpath):
        if fnmatch.fnmatch(file, '*.json') or fnmatch.fnmatch(file, '*.yml'):
            yield(file)


def _read_file(fpath):
    """
    Read a file a literaly return content.

    If file is yaml, it must skip the stream header.
    """
    with open(fpath, 'r') as f:
        # skip '---' header of yaml streams
        if os.path.splitext(fpath)[1] == ".yml":
            f.readline()

        # eat up every empty lines
        pos = f .tell()
        line = f.readline()

        while not line.strip():
            pos = f .tell()
            line = f.readline()

        # go back to non-empty line
        f.seek(pos)

        return f.read()


def _read_files(dpath, verbose):
    """
    Read every files *{json,yml} files under a given directory.

    Return a list of dictionaries. Each dictionary contains the filename and
    the file content.
    """
    if os.path.isdir(dpath):
        dfiles = []
        for f in _get_filenames(dpath):
            if verbose:
                print("Reading file " + os.path.join(dpath, f))
            dfiles.append({"filename": f,
                           "content": _read_file(os.path.join(dpath, f))})
        return dfiles
    else:
        return None
        if verbose:
            print(dpath + " directory doesn't exist...skipping")

# def make_doc_dir():
#     """Create docs folder inside role."""
#     docdir = path.abspath(rolepath + "/docs")

#     # make sure destination exist, if not create it
#     if not path.isdir(symlink_target):
#         mkdir(symlink_target,'755')


def _make_role_symlink(rolepath, target, verbose):
    """
    Add symlink for each roles.

    since '../' cannot be use in a sphinx toctree, this will for a given role
    create a symlink from the <playbook_dir>/docs to
    <playbook_dir>/roles/rolename/docs/index.
    """
    # symlink src
    symlink_target = os.path.abspath(os.path.join(rolepath, target))

    # symlink dst
    symlink_name = "role-" + os.path.basename(rolepath) + "-" + target

    if verbose:
        print("Generating symlink to role " + symlink_target + " ...")

    if not os.path.islink(symlink_name):
        os.symlink(symlink_target, symlink_name)


def make_role_doc(rolepath, **kwargs):
    """
    Generate documentation on the fly for a single role.

    Informations are picked in defaults/main.yml and meta/main.yml.
    """
    verbose = kwargs.get('verbose')
    dry_run = kwargs.get('dry_run')
    target = kwargs.get('target')

    role = os.path.basename(rolepath)

    print("Generating doc for role " + role + "...")
    if verbose:
        print("Current rolepath is : " + rolepath)

    # create symlink if needed
    if target:
        _make_role_symlink(rolepath, target, verbose)

    # load meta/main.yml
    meta_file = os.path.join(rolepath, "meta/main.yml")
    if os.path.isfile(meta_file):
        metainfos = _load_yml_file(meta_file)
        if verbose:
            print("Loaded role meta/main.yml: \n\n")
            print(metainfos)
            print("\n")
    else:
        metainfos = None
        if verbose:
            print(meta_file + " doesn't exist...")

    # load files in vars/*
    vars_files = _read_files(os.path.join(rolepath, "vars"), verbose)

    # load defaults/*
    defaults_files = _read_files(os.path.join(rolepath, "defaults"), verbose)

    # load template and create templating environment
    env = Environment(loader=PackageLoader('ansidoc', 'templates'),
                      lstrip_blocks=True,
                      trim_blocks=True)

    # render readme
    template = env.get_template('readme.j2')

    t = template.render(metainfos, role_vars=vars_files,
                        role_defaults=defaults_files)

    if verbose or dry_run:
        print(t)

    # create readme file in rolepath/docs
    # makedirs(path.abspath(rolepath + "/docs"), mode=755, exist_ok=False)

    # create readme file in rolepath/README.md
    if not dry_run:
        _write_file(t, os.path.join(rolepath, "README.md"))

    print("Role " + role + " ...done\n")
