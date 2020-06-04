#!/usr/bin/env python3

import yaml
import connections.irc
import connections.matrix
# TODO: these last two imports are important, to run the decorators. 
#       Is there a better solution?
from connections import create_bots

botdict = []


def loadConfig(filename: str = "mtibb.yaml"):
    """
        Loads the config file for the mtibb bot.
        This file usually resides in the project directory as ``mtibb.yaml``
        but can also be changed.
    """
    with open(filename) as f:
        config = yaml.safe_load(f)
    # TODO: Check if config is valid
    return config


def message_handler(source: str, sender: str, content: str) -> None:
    print(source + " Message from " + sender + " saying: " + content)
    for bot in botdict:
        if bot != source:
            # Relay Message!
            print("Relay Message from " + source + " to " + bot)
            pass


def main():
    conf = loadConfig()
    # start bots
    global botdict  # TODO: obviously eliminate this though new class or smth.
    botdict = create_bots(
        configuration=conf['Connections'],
        msg_handler=message_handler
    )

    while True:
        pass


if __name__ == "__main__":
    main()
