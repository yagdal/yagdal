import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

from pkg_resources import parse_version
from setuptools import Extension, setup

GDAL_MIN_VERSION = parse_version("3.4.0")
CURRENT_FILE_PATH = Path(__file__).absolute().parent


def get_gdal_version(gdal_dir: Path) -> str:
    gdal_version = os.environ.get("GDAL_VERSION")
    if gdal_version:
        return gdal_version
    gdalinfo = gdal_dir / "bin" / "gdalinfo"
    gdal_ver = subprocess.check_output(
        [str(gdalinfo), "--version"], stderr=subprocess.STDOUT
    ).decode("ascii")
    return (gdal_ver.split()[1]).strip(",")


def check_gdal_version(gdal_version: str) -> None:
    """checks that the GDAL library meets the minimum version"""
    if parse_version(gdal_version) < GDAL_MIN_VERSION:
        raise SystemExit(
            f"ERROR: Minimum supported GDAL version is {GDAL_MIN_VERSION}, installed "
            f"version is {gdal_version}. For more information see: "
            "https://yagdal.github.io/yagdal/stable/installation.html"
        )


def get_gdal_dir() -> Path:
    """
    This function finds the base GDAL directory.
    """
    gdal_dir_environ = os.environ.get("GDAL_DIR")
    gdal_dir: Optional[Path] = None
    if gdal_dir_environ is not None:
        gdal_dir = Path(gdal_dir_environ)
    elif gdal_dir is None:
        gdalinfo = shutil.which("gdalinfo", path=sys.prefix)
        if gdalinfo is None:
            gdalinfo = shutil.which("gdalinfo")
        if gdalinfo is None:
            raise SystemExit(
                "gdalinfo executable not found. Please set the GDAL_DIR variable. "
                "For more information see: "
                "https://yagdal.github.io/yagdal/stable/installation.html"
            )
        gdal_dir = Path(gdalinfo).parent.parent
    elif gdal_dir is not None and gdal_dir.exists():
        print("GDAL_DIR is set, using existing GDAL installation..\n")
    else:
        raise SystemExit(f"ERROR: Invalid path for GDAL_DIR {gdal_dir}")
    return gdal_dir


def get_gdal_libdirs(gdal_dir: Path) -> List[str]:
    """
    This function finds the library directories
    """
    gdal_libdir = os.environ.get("GDAL_LIBDIR")
    libdirs = []
    if gdal_libdir is None:
        libdir_search_paths = (gdal_dir / "lib", gdal_dir / "lib64")
        for libdir_search_path in libdir_search_paths:
            if libdir_search_path.exists():
                libdirs.append(str(libdir_search_path))
        if not libdirs:
            raise SystemExit(
                "ERROR: GDAL_LIBDIR dir not found. Please set GDAL_LIBDIR."
            )
    else:
        libdirs.append(gdal_libdir)
    return libdirs


def get_gdal_incdirs(gdal_dir: Path) -> List[str]:
    """
    This function finds the include directories
    """
    gdal_incdir = os.environ.get("GDAL_INCDIR")
    incdirs = []
    if gdal_incdir is None:
        if (gdal_dir / "include").exists():
            incdirs.append(str(gdal_dir / "include"))
        else:
            raise SystemExit(
                "ERROR: GDAL_INCDIR dir not found. Please set GDAL_INCDIR."
            )
    else:
        incdirs.append(gdal_incdir)
    return incdirs


def get_cythonize_options():
    """
    This function gets the options to cythonize with
    """
    # Configure optional Cython coverage.
    cythonize_options = {
        "language_level": sys.version_info[0],
        "compiler_directives": {
            "c_string_type": "str",
            "c_string_encoding": "utf-8",
            "embedsignature": True,
        },
    }
    if os.environ.get("YAGDAL_FULL_COVERAGE"):
        cythonize_options["compiler_directives"].update(linetrace=True)
        cythonize_options["annotate"] = True
    return cythonize_options


def get_libraries(libdirs: List[str]) -> List[str]:
    """
    This function gets the libraries to cythonize with
    """
    libraries = ["gdal"]
    if os.name == "nt":
        for libdir in libdirs:
            projlib = list(Path(libdir).glob("gdal*.lib"))
            if projlib:
                libraries = [str(projlib[0].stem)]
                break
    return libraries


def get_extension_modules():
    """
    This function retrieves the extension modules
    """
    if "clean" in sys.argv:
        return None

    # make sure cython is available
    try:
        from Cython.Build import cythonize
    except ImportError:
        raise SystemExit(
            "ERROR: Cython.Build.cythonize not found. "
            "Cython is required to build yagdal."
        )

    # By default we'll try to get options GDAL_DIR or the local version of proj
    gdal_dir = get_gdal_dir()
    library_dirs = get_gdal_libdirs(gdal_dir)
    include_dirs = get_gdal_incdirs(gdal_dir)

    gdal_version = get_gdal_version(gdal_dir)
    check_gdal_version(gdal_version)
    gdal_version_major, gdal_version_minor, gdal_version_patch = parse_version(
        gdal_version
    ).base_version.split(".")

    # setup extension options
    ext_options = {
        "include_dirs": include_dirs,
        "library_dirs": library_dirs,
        "runtime_library_dirs": library_dirs if os.name != "nt" else None,
        "libraries": get_libraries(library_dirs),
    }
    # setup cythonized modules
    return cythonize(
        [
            Extension("yagdal._compat", ["yagdal/_compat.pyx"], **ext_options),
            Extension("yagdal._version", ["yagdal/_version.pyx"], **ext_options),
        ],
        quiet=True,
        compile_time_env={
            "CTE_GDAL_VERSION_MAJOR": int(gdal_version_major),
            "CTE_GDAL_VERSION_MINOR": int(gdal_version_minor),
            "CTE_GDAL_VERSION_PATCH": int(gdal_version_patch),
            "CTE_PYTHON_IMPLEMENTATION": platform.python_implementation(),
        },
        **get_cythonize_options(),
    )


def get_package_data() -> Dict[str, List[str]]:
    """
    This function retrieves the package data
    """
    # setup package data
    package_data = {"yagdal": ["*.pyi", "py.typed"]}
    if (
        os.environ.get("YAGDAL_WHEEL") is not None
        and (CURRENT_FILE_PATH / "yagdal" / ".lib").exists()
    ):
        package_data["yagdal"].append(os.path.join(".lib", "*"))
    return package_data


def get_version():
    """
    retreive yagdal version information (taken from Fiona)
    """
    with open(Path("yagdal", "__init__.py"), "r") as f:
        for line in f:
            if line.find("__version__") >= 0:
                # parse __version__ and remove surrounding " or '
                return line.split("=")[1].strip()[1:-1]
    raise SystemExit("ERROR: yagdal version not found.")


# static items in setup.cfg
setup(
    version=get_version(),
    ext_modules=get_extension_modules(),
    package_data=get_package_data(),
)
