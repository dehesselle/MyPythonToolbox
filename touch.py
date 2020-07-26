# SPDX-License-Identifier: MIT
# https://github.com/dehesselle/MyPythonToolbox


import os


def touch(path):
    """Simplified equivalent of coreutil's 'touch' command."""
    with open(path, 'a'):
        os.utime(path, None)
