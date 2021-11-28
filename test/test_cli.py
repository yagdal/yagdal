import os
import subprocess
import sys
from contextlib import contextmanager

import pytest

YAGDAL_CLI_ENDPONTS = pytest.mark.parametrize(
    "input_command", [["yagdal"], [sys.executable, "-m", "yagdal"]]
)


@contextmanager
def tmp_chdir(new_dir):
    """
    This temporarily changes directories when running the tests.
    Useful for when testing wheels in the yagdal directory
    when yagdal has not been build and prevents conflicts.
    """
    curdir = os.getcwd()
    try:
        os.chdir(new_dir)
        yield
    finally:
        os.chdir(curdir)


@pytest.mark.cli
@YAGDAL_CLI_ENDPONTS
def test_main(input_command, tmpdir):
    with tmp_chdir(str(tmpdir)):
        output = subprocess.check_output(
            input_command, stderr=subprocess.STDOUT
        ).decode("utf-8")
    assert "yagdal version:" in output
    assert "GDAL version:" in output
    assert "-v, --verbose  Show verbose debugging version information." in output


@pytest.mark.cli
@YAGDAL_CLI_ENDPONTS
@pytest.mark.parametrize("option", ["-v", "--verbose"])
def test_main__verbose(input_command, option, tmpdir):
    with tmp_chdir(str(tmpdir)):
        output = subprocess.check_output(
            input_command + [option], stderr=subprocess.STDOUT
        ).decode("utf-8")
    assert "yagdal:" in output
    assert "GDAL:" in output
    assert "PROJ:" in output
    assert "GEOS:" in output
    assert "System" in output
    assert "python" in output
    assert "Python deps" in output
    assert "-v, --verbose " not in output
