import os
import sys
import contextlib

PLUGIN_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
LIB_DIRECTORY = os.path.join(PLUGIN_DIRECTORY, "lib")

@contextlib.contextmanager
def import_bundled(packages_path=LIB_DIRECTORY):
    sys.path.insert(0, packages_path)
    try:
        yield
    finally:
        sys.path.remove(packages_path)
