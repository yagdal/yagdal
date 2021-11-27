.. highlight:: shell

============
Installation
============


Installing from source
======================

Setup GDAL
------------

GDAL is required when building from source.

:ref:`GDAL Installation Instructions <download>`

You can also download GDAL from:

-  https://download.osgeo.org/gdal
-  https://github.com/OSGeo/GDAL


Additionally, you can use `conda <https://conda.io/en/latest/>`__ with the `conda-forge <https://conda-forge.org/>`__ channel:

  .. code-block:: bash

      conda config --prepend channels conda-forge
      conda config --set channel_priority strict
      conda create -n yagdal_env libgdal cython
      conda activate yagdal_env

  .. note::
      "... we recommend always installing your packages inside a
      new environment instead of the base environment from
      anaconda/miniconda. Using envs make it easier to
      debug problems with packages and ensure the stability
      of your root env."
        -- https://conda-forge.org/docs/user/tipsandtricks.html



yagdal Build Environment Variables
-----------------------------------

.. envvar:: GDAL_VERSION

    This sets the version of GDAL when building yagdal. This
    enables installing yagdal when the GDAL executables are not
    present but the header files exist.

.. envvar:: GDAL_DIR

    This is the path to the base directory for GDAL.
    Examples of how to set the GDAL_DIR environment variable:

    Windows::

        set GDAL_DIR=C:\OSGeo4W\

    Linux::

        export GDAL_DIR=/usr/local

.. envvar:: GDAL_LIBDIR

    This is the path to the directory containing the GDAL libraries.
    If not set, it searches the `lib` and `lib64` directories inside
    the GDAL directory.

.. envvar:: GDAL_INCDIR

    This is the path to the GDAL include directory. If not set, it assumes
    it is the `includes` directory inside the GDAL directory.

.. envvar:: YAGDAL_WHEEL

    This is a boolean value used when building a wheel.

.. envvar:: YAGDAL_FULL_COVERAGE

    Boolean that sets the compiler directive for cython to include
    the test coverage.


Setup yagdal
------------

In the setup.py, the order for searching for GDAL is:

    1. The :envvar:`GDAL_DIR` environment variable
    2. The `gdalinfo` executable in sys.prefix
    3. The `gdalinfo` executable on the PATH

For best results, set the :envvar:`GDAL_DIR` environment variable to
point to location of GDAL installation before running setup.py.


Install yagdal
~~~~~~~~~~~~~~

.. note:: `Cython <http://cython.org/>`_ or pip>=10.0.1 is required for the installation.

.. note:: You may need to run pip with administrative privileges (e.g. `sudo pip`) or
          perform a user only installation (e.g. `pip install --user`).


From GitHub with `pip`:
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    pip install git+https://github.com/yagdal/yagdal.git

From cloned GitHub repo for development:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    pip install -e .
