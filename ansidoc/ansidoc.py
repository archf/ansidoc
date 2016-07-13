import sys

# fixme: import only safe_load
# from yaml import yaml.safe_load
import yaml
from jinja2 import Environment, PackageLoader, FileSystemLoader

# to convert markdown to rst
# import yaml2rst

# from m2r import M2R
# m2r = M2R()

# # def gen_toctree(title,text):
# #     toc = open("../roles/" + title + "/docs/index.rst",'w')
# #     toc.write(m2r("## " + title))
# #     toc.write(TOCTREE_TEMPLATE)

#     # adding a symlink for each roles
#     if not path.islink(element + "-docs"):
#         os.symlink(path.abspath('..') + "/roles/" + element + "/docs", \
#                    element + "-docs")

#         outfile.write(yaml2rst.convert_text(infile.read()))

#         # generate a toctree for each roles
#         # gen_toctree(element, TOCTREE_TEMPLATE)


def _load_yml_file(path):
    """ safe_load yaml file """

    with open(path, 'r') as stream:
        return yaml.safe_load(stream)


def _write_file(data, filepath):
    """ write a file to disk only if content has changed """

    with open(filepath, 'r+') as f:
        # replace content only if needed
        if data != f.read():
            f.truncate(0)
            f.seek(0)
            f.write(data)


def make_role_doc(rolepath):

    """
    Generate documentation on the fly for a single role based on Ansible default
    variables and meta/main.yml
    """

    # load defaults/main.yml file
    if path.isfile(rolepath + "/defaults/main.yml"):
        with open(rolepath + "/defaults/main.yml", 'r') as f:
            # fixme: "skip ---\n in a better way"
            f.seek(5)
            default_vars = f.read()

    # load meta/main.yml
    if path.isfile(rolepath + "/meta/main.yml"):
        metainfo = _load_yml_file(rolepath + "/meta/main.yml")
        print(metainfo)

    # load template and create templating environment
    env = Environment(loader=FileSystemLoader('ansidoclib'),
                      lstrip_blocks='true', trim_blocks='true')

    # render readme
    template = env.get_template('readme.j2')

    _write_file(template.render(metainfo, role_default_vars=default_vars),
                rolepath + '/README.md')
    # env = Environment(loader=PackageLoader('yourapplication', 'templates'))


def ansidoc(args):
    # this only works if roles_path basename is 'roles'
    # check wether give path is a rolepath or a roledir
    path = args.path
    if path.basename(path) == 'roles':

        for role in os.listdir(path):
            print("processing " + role + "...")
            make_role_doc(role)
    else:
        make_role_doc(path)
