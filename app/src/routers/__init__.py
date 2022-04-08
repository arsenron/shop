from os.path import dirname, basename, isfile, join, isdir
import glob


modules = glob.glob(join(dirname(__file__), "*.py"))
modules = [
    basename(m)[:-3]
    for m in modules
    if isfile(m) and not m.endswith("__init__.py") and not m.endswith("-bak.py")
]

packages = glob.glob(join(dirname(__file__), "*"))
packages = [basename(m) for m in packages if isdir(m) and not m.endswith("__pycache__")]

__all__ = modules
