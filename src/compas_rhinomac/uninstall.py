from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

import compas_rhinomac
import compas_rhinomac.install

from compas._os import remove_symlink


__all__ = ['uninstall']


def uninstall(packages=None):
    """Uninstall COMPAS from Rhino.

    Parameters
    ----------
    packages : list of str
        List of packages to uninstall.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhinomac.uninstall()

    .. code-block:: python

        $ python -m compas_rhinomac.uninstall

    """
    if not packages:
        # should this not default to all installed compas packages?
        packages = compas_rhinomac.install.INSTALLABLE_PACKAGES

    print('Uninstalling COMPAS packages from RhinoMac IronPython Lib.')

    ipylib_path = compas_rhinomac._get_ironpython_lib_path()

    results = []
    exit_code = 0

    for package in packages:
        symlink_path = os.path.join(ipylib_path, package)

        if not os.path.exists(symlink_path):
            continue

        try:
            remove_symlink(symlink_path)
            results.append((package, 'OK'))
        except OSError:
            results.append((package, 'ERROR: Cannot remove symlink, try to run as administrator.'))

    for _, status in results:
        if status is not 'OK':
            exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'WARNING: One or more packages failed, will not uninstall bootstrapper.'))
    else:
        compas_bootstrapper = os.path.join(ipylib_path, 'compas_bootstrapper.py')
        try:
            if os.path.exists(compas_bootstrapper):
                os.remove(compas_bootstrapper)
                results.append(('compas_bootstrapper', 'OK'))
        except:
            results.append(('compas_bootstrapper', 'ERROR: Could not delete compas_bootstrapper'))

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

    parser.add_argument('-p', '--packages', nargs='+', help="The packages to uninstall.")

    args = parser.parse_args()

    uninstall(args.packages)
