import pytest
import os
from ansidoc import ansidoclib


@pytest.fixture(scope="module")
def roledir(request):
    dirpath = os.path.split(str(request.fspath))[0]
    rolename = "fake-role"
    return os.path.join(dirpath, rolename)
    # print(fspath)
    # fn = ansidoclib._get_filenames("defaults")
    # assert fn == "main.yml"


def test_load_yml_file(roledir):
    content = ansidoclib._load_yml_file(os.path.join(roledir,
                                                     "defaults/main.yml"))
    assert content["fake_role_pkg_state"] == "latest"


def test_write_file():
    pass


def test_get_filenames(roledir):
    for i in ansidoclib._get_filenames(os.path.join(roledir, "vars")):
        assert i in ["RedHat.yml", "Debian.yml"]


def test_read_file():
    pass


def test_read_files():
    pass


def test_make_role_symlink():
    pass
