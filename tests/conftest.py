import pytest
import os


@pytest.fixture(scope="module")
def roledir(request):
    dirpath = os.path.split(str(request.fspath))[0]
    rolename = "fake-role"
    return os.path.join(dirpath, rolename)
