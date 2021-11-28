"""
This is the main entry point for yagdal CLI

e.g. python -m yagdal

"""

import argparse

from yagdal import __gdal_version__, __version__, _show_versions

parser = argparse.ArgumentParser(
    description=f"yagdal version: {__version__} [GDAL version: {__gdal_version__}]"
)
parser.add_argument(
    "-v",
    "--verbose",
    help="Show verbose debugging version information.",
    action="store_true",
)


def main():
    """
    Main entrypoint into the command line interface.
    """
    args = parser.parse_args()
    if args.verbose:
        _show_versions.show_versions()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
