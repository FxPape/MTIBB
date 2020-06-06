#!/usr/bin/env python3

import sys
import yaml
from connections import create_bots
from typing import Dict
from handlers import handler
from helpers import message


def loadConfig(filename: str = "mtibb.yaml") -> Dict['str', Dict]:
    """
    Loads the config file for the mtibb bot.
    This file usually resides in the project directory as ``mtibb.yaml``
    but can also be changed.
    """
    try:
        with open(filename) as f:
            config = yaml.safe_load(f)
        # TODO: Check if config is valid
    except FileNotFoundError:
        print(
            "No config file found. Please rename mtibb.sample.yaml" +
            " to mtibb.yaml and adapt the values to your use case"
        )
        sys.exit(1)
    return config


class Bridge_bot:
    botdict = {}
    message_handler = None
    conf = {}

    def __message_handler_pre(self, msg: message):
        if self.message_handler is None:
            self.message_handler = handler(
                self.conf['Settings'],
                self.botdict
            )
        self.message_handler.message_handler(msg)

    def main(self):
        # Argparse config file location? Not too important atm
        self.conf = loadConfig()
        # start bots
        self.botdict = create_bots(
            configuration=self.conf['Connections'],
            msg_handler=self.__message_handler_pre
        )

        while True:
            pass


if __name__ == "__main__":
    bridge = Bridge_bot()
    bridge.main()
