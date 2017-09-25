import pytest
import os
from ansidoc import helpers


def test_load_yml_file(roledir):
    """Test yml file loading."""
    content = helpers.load_yml_file(os.path.join(roledir,
                                                 "defaults/main.yml"),
                                    verbose=False)
    assert content["fake_role_pkg_state"] == "latest"

# using tmpdir fixture, test both helpers.write_file and helpers.write_file
def test_write_file(tmpdir):
    tmpfile = os.path.join(str(tmpdir), "tmpfile")
    helpers.write_file("content", tmpfile)

    # read timestamp
    mtime = os.lstat(tmpfile).st_mtime
    # write again
    helpers.write_file("content", tmpfile)

    # validate content
    assert helpers.read_file(tmpfile) == "content"

    # make sure timestamp has not changed
    assert os.lstat(tmpfile).st_mtime == mtime


def test_get_filenames(roledir):
    """Retreive all files in role /vars/*."""
    for i in helpers.get_filenames(os.path.join(roledir, "vars"), '*.yml'):
        assert i in ["RedHat.yml", "Debian.yml"]


def test_make_role_symlink():
    pass
