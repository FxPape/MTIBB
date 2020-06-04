#!/usr/bin/env python3

import yaml
from connections.irc import irc_bot
from connections.matrix import matrix_bot
import asyncio


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


async def main():
    conf = loadConfig()
    # start bots
    # ibot = irc_bot(
    #     conf=conf['Connections']['IRC'],
    #     msg_handler=message_handler
    # )
    mbot = matrix_bot(conf['Connections']['Matrix'])
    await mbot.login()
    await mbot.sync_forever()
  
    # ibot.start() # This is busy waiting, but in thread


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
