"""
Yet another GDAL Python Wrapper
"""

__version__ = "0.0.0"

from yagdal._show_versions import (  # noqa: F401 pylint: disable=unused-import
    show_versions,
)
from yagdal._version import get_gdal_version_info, get_geos_version, get_proj_version

__gdal_version__ = get_gdal_version_info("RELEASE_NAME")
GDAL_VERSION = tuple(int(version) for version in __gdal_version__.split("."))
PROJ_VERSION = get_proj_version()
__proj_version__ = ".".join([str(version) for version in PROJ_VERSION])
GEOS_VERSION = get_geos_version()
__geos_version__ = ".".join([str(version) for version in GEOS_VERSION])
