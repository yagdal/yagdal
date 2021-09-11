"""
Methods accessing GDAL and its libraries version information.
"""

from yagdal._compat cimport cstrencode


def get_gdal_version_info(str key not None):
    """

    Available keys:

        - VERSION_NUM: Returns GDAL_VERSION_NUM formatted as a string.
        - RELEASE_DATE: Returns GDAL_RELEASE_DATE formatted as a string.
          i.e. “20020416”.
        - RELEASE_NAME: Returns the GDAL_RELEASE_NAME. ie. “1.1.7”
        - –version: Returns one line version message suitable for use
          in respons to version requests. i.e. “GDAL 1.1.7, released 2002/04/16”
        - LICENSE: Returns the content of the LICENSE.TXT file
          from the GDAL_DATA directory.
        - BUILD_INFO: List of NAME=VALUE pairs separated by newlines with
          information on build time options.

    Parameters
    ----------
    key: str
        The type of version info.

    Returns
    -------
    Optional[str]:
        The version information if available.
    """
    cdef const char* version_information = GDALVersionInfo(cstrencode(key))
    if version_information == NULL:
        return None
    return version_information


def get_proj_version():
    """
    Get PROJ Version

    Returns
    -------
    Tuple[int, int, int]:
        major, minor, patch
    """
    cdef:
        int major = 0
        int minor = 0
        int patch = 0
    OSRGetPROJVersion(&major, &minor, &patch)
    return major, minor, patch


def get_geos_version():
    """
    Get GEOS Version

    Returns
    -------
    Tuple[int, int, int]:
        major, minor, patch
    """
    cdef:
        int major = 0
        int minor = 0
        int patch = 0
    OGRGetGEOSVersion(&major, &minor, &patch)
    return major, minor, patch
