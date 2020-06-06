"""
Module containing helper functions needed by other modules
"""
import importlib
import pkgutil
import types
from typing import Dict


def import_submodules(
    package,
    recursive: bool = True
) -> Dict[str, types.ModuleType]:
    """
    Import all submodules of a module, recursively, including subpackages

    This is neccessary to import and register all available bot/connection
    types

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


class message:
    source: str = ""
    sender: str = ""
    content: str = ""
    time: int = 0

    def __init__(self, source, sender, content, time=0):
        self.source = source
        self.sender = sender
        self.content = content
        self.time = time
