"""
Contains all the connection logic for the supported networks.

Each network connection is defined in a seperate submodule and
registered here via the register_type decorator.
Using the typename given there the class will automatically be used
as handler of servers with the same "type" field

Each submodule *must* implement abc_connection (mostly for typeing)
"""
import threading
from typing import Callable, Dict
from abc import ABC, abstractmethod
import importlib
import pkgutil
import types

type_lookup = {}


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


class abc_connection(ABC):
    @abstractmethod
    def __init__(
        self,
        name: str,
        conf: Dict['str', Dict],
        msg_handler: Callable[[str, str, str], None]
    ):
        """
        Initializes everything needed to start a connection.
        This does NOT start the connection, that's what `start()` is for.

        :param name:
         Name of the connection. Will be given the name of
         the according configuration block in the yaml configuration.
        :param conf:
         Dict containing everything in the connections block
         of the configuration (i.e.: including type but excluding name!)
        :param msg_handler:
         Callback for handling any incoming message.
         Parameters are this connections name, the sending client and
         the message itself.
        :type name: str
        :type conf: Dict[str]
        :type msg_handler: Callable[[str, str, str], None]
        """
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def post(self, message: str) -> None:
        pass


def register_type(contype: str):
    def decor(f):
        if not issubclass(f, abc_connection):
            raise RuntimeError(
                '''
                Connection classes registered with register_type must be
                abc_connection subclasses
                '''
            )
        type_lookup[contype] = f
        return f
    return decor


def create_bots(
    configuration: Dict,
    msg_handler: Callable[[str, str, str], None]
) -> Dict[str, abc_connection]:
    # print(type_lookup)
    botdict = {}
    for name in configuration:
        contype = configuration[name]['type']
        conclass = type_lookup[contype]
        botdict[name] = conclass(name, configuration[name], msg_handler)
        thrd = threading.Thread(target=botdict[name].start)
        thrd.daemon = True
        thrd.start()
    return botdict


# Load all submodules in this folder when this module is imported
import_submodules(__name__)
