import os
import fnmatch
import yaml


def load_yml_file(fpath, verbose):
    """safe_load a yaml file."""

    try:
        with open(fpath, 'r') as stream:
            content = yaml.safe_load(stream)
        if verbose:
            print("Loaded '%s':\n" % fpath)
            print(content)
            print("\n")
    except FileNotFoundError as e:
        content = None
        print(e)

    return content

def load_yml_files(dpath, verbose):
    """
    Safe load multiple yaml files.

    All top level values are expected to be keys.
    """
    if os.path.isdir(dpath):
        content = {}
        for f in get_filenames(dpath, '*.yml'):
            content = {**content, **load_yml_file(os.path.join(dpath, f), verbose)}
    return content


def write_file(data, fpath):
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


def get_filenames(dpath, pattern):
    """Yield files in given directory matching pattern."""
    for file in os.listdir(dpath):
        if pattern == '*.yml':
            if fnmatch.fnmatch(file, pattern) or fnmatch.fnmatch(file, '*.yaml'):
                yield (file)
        elif pattern == '*.json':
            if fnmatch.fnmatch(file, pattern) or fnmatch.fnmatch(file, '*.jsn'):
                yield (file)
        elif pattern == '*.md':
            if fnmatch.fnmatch(file, pattern):
                yield (file)


def read_file(fpath):
    """
    Read a file and literaly return content.

    If file is yaml, it must skip the stream header.
    """
    with open(fpath, 'r') as f:
        # skip '---' header of yaml streams
        if os.path.splitext(fpath)[1] == ".yml":
            f.readline()

        # eat up every empty lines
        pos = f.tell()
        line = f.readline()

        while not line.strip():
            pos = f.tell()
            line = f.readline()

        # go back to non-empty line
        f.seek(pos)

        return f.read()



def read_files(dpath, type, verbose):
    """
    Read every files files under a given directory.
     Return a list of dictionaries. Each dictionary contains the filename
    and the file content.
    """
    if os.path.isdir(dpath):
        dfiles = []
        for f in get_filenames(dpath, type):
            if verbose:
                print("Reading file '%s'" % os.path.join(dpath, f))
            dfiles.append(
                {"filename": f, "content": read_file(os.path.join(dpath, f))})
        return dfiles
    else:
        return None
        if verbose:
            print("'%s' directory doesn't exist...skipping" % dpath)
