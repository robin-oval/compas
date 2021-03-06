from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import importlib
import os
import sys

import compas_rhino

from compas._os import remove_symlink
from compas._os import create_symlink


__all__ = ['install']


INSTALLABLE_PACKAGES = ['compas', 'compas_rhino', 'compas_ghpython']


def _get_package_path(package):
    return os.path.abspath(os.path.join(os.path.dirname(package.__file__), '..'))


def install(version=None, packages=None):
    """Install COMPAS for Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0'}, optional
        The version number of Rhino.
        Default is ``'6.0'``.
    packages : list of str, optional
        List of packages to install or None to use default package list.
        Default is ``['compas', 'compas_rhino', 'compas_ghpython']``.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhino.install('6.0')

    .. code-block:: python

        $ python -m compas_rhino.install 6.0

    """
    if version not in ('5.0', '6.0'):
        version = '6.0'

    if not packages:
        packages = INSTALLABLE_PACKAGES

    print('Installing COMPAS packages to Rhino {0} IronPython lib:'.format(version))

    ipylib_path = compas_rhino._get_ironpython_lib_path(version)

    results = []
    exit_code = 0

    for package in packages:
        # why is this necessary?
        # why does the package path return the path to the parent
        # only to concatenate it here with the package name again
        base_path = _get_package_path(importlib.import_module(package))

        package_path = os.path.join(base_path, package)
        symlink_path = os.path.join(ipylib_path, package)

        if os.path.exists(symlink_path):
            try:
                remove_symlink(symlink_path)
            except OSError:
                results.append((package, 'ERROR: Cannot remove symlink, try to run as administrator.'))

        try:
            create_symlink(package_path, symlink_path)
            results.append((package, 'OK'))
        except OSError:
            results.append((package, 'ERROR: Cannot create symlink, try to run as administrator.'))

    for _, status in results:
        if status is not 'OK':
            exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'WARNING: One or more packages failed, will not install bootstrapper, try uninstalling first'))
    else:
        conda_prefix = os.environ.get('CONDA_PREFIX', None)
        compas_bootstrapper = os.path.join(ipylib_path, 'compas_bootstrapper.py')
        try:
            with open(compas_bootstrapper, 'w') as f:
                f.write('CONDA_PREFIX = r"{0}"'.format(conda_prefix))
                results.append(('compas_bootstrapper', 'OK'))
        except:
            results.append(('compas_bootstrapper', 'ERROR: Could not create compas_bootstrapper to auto-determine Python environment'))

    for package, status in results:
        print('   {} {}'.format(package.ljust(20), status))

        if status is not 'OK':
            exit_code = -1

    print('\nCompleted.')
    sys.exit(exit_code)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version', choices=['5.0', '6.0'], default='5.0', help="The version of Rhino to install the packages in.")
    parser.add_argument('-p', '--packages', nargs='+', help="The packages to install.")

    args = parser.parse_args()

    install(version=args.version, packages=args.packages)
