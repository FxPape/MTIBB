"""
Contains all the connection logic for the supported networks.

Each network connection is defined in a seperate submodule and
registered here via the register_type decorator.
Using the typename given there the class will automatically be used
as handler of servers with the same "type" field
"""
import threading
from typing import Callable, Dict

type_lookup = {}


def register_type(contype: str):
    def decor(f):
        type_lookup[contype] = f
        return f
    return decor


def create_bots(
    configuration: Dict,
    msg_handler: Callable[[str, str, str], None]
) -> Dict:
    print(type_lookup)
    botdict = {}
    for name in configuration:
        contype = configuration[name]['type']
        conclass = type_lookup[contype]
        botdict[name] = conclass(name, configuration[name], msg_handler)
        threading.Thread(target=botdict[name].start).start()
    return botdict
