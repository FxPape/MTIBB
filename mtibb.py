#!/usr/bin/env python3

import yaml
from connections.irc import irc_bot
from connections.matrix import matrix_bot
import threading
import sys


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


def main():
    conf = loadConfig()
    # start bots
    # TODO: Idee: Connections klasse, die nur conf['Connections']
    #       Bekommt und daraus ALLES baut.
    #       Dann wären noch mehr Netzwerke einfach einbaubar.
    Networks = {
        "IRC": irc_bot(
            conf=conf['Connections']['IRC'],
            msg_handler=message_handler
        ),
        "Matrix": matrix_bot(
            conf=conf['Connections']['Matrix'],
            msg_handler=message_handler
        )
    }
    for service in Networks.values():
        threading.Thread(target=service.start).start()

    while True:
        x = input()
        if x != '':
            sys.exit(0)


if __name__ == "__main__":
    main()
