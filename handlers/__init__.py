"""
This module contains all Message Handling and Command execution
"""
from typing import Dict
from connections import abc_connection
from helpers import message


class handler:
    botdict: Dict[str, abc_connection] = {}

    def __init__(self, config, botdict: Dict[str, abc_connection]):
        self.botdict = botdict
        self.config = config

    def message_handler(self, msg: message) -> None:
        """
        The message handler. Currently very stupidly relaying
        everything it gets. Should dispatch into other functions/methods
        """
        # print(source + " Message from " + sender + " saying: " + content)
        # I need some source -> destination mapping
        if msg.content.startswith('!'):  # ! should modify message forwarding
            pass
        for bot in self.botdict:
            if bot != msg.source:
                # Relay Message!
                # print("Relay Message from " + source + " to " + bot)
                self.botdict[bot].post(
                    f"[{msg.source}] {msg.sender} | {msg.content}"
                )
        if msg.content.startswith('?'):  # all commands start with ?
            pass
