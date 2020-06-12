"""
This module contains all Message Handling and Command execution
"""
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Tuple

from connections import abc_connection
from helpers import import_submodules, message

handler_instance = None


class command_response:
    silent: bool = False
    reply_message: str = ""
    config_changes: bool = False

    def __str__(self) -> str:
        return self.reply_message

    def __init__(self, result: str = ""):
        self.reply_message = result
        self.silent = (result == "")

    def isMultiline(self):
        return '\n' in self.reply_message


class command_handler(ABC):
    message_handler = None

    def __init__(self, handler_instance):
        """
        Since during import of this module each handler will be initialized
        they all need this constructor.
        """
        self.message_handler = handler_instance

    @abstractmethod
    def __str__(self):
        return """ This should explain the command"""

    @abstractmethod
    def handle(self, message: message) -> command_response:
        pass


def register_commands(command_names: List[str]):
    if handler_instance is None:
        raise RuntimeError(
            """Only import command handlers after the message handler
            (handlers.message_handler) was initialized"""
        )

    def decor(f: Callable):
        if issubclass(f, command_handler):
            cmdhandler = f(handler_instance)
            for command_name in command_names:
                handler_instance.commands[command_name] = cmdhandler
            return f
        else:
            raise ValueError(
                "Decorated class must be subtype of handlers.command_handler!"
            )
    return decor


def register_command(command_name: str):
    return register_commands([command_name])


def require_admin(f: Callable):
    def gated(self, msg: message):
        admins = self.message_handler.administrators
        if (msg.source, msg.sender) not in admins:
            return command_response('Only bot admins can use this command')
        else:
            return f(self, msg)
    return gated


class message_handler:
    botdict: Dict[str, abc_connection] = {}
    no_forward_user: List[Tuple[str, str]] = []
    no_forward_source: List[str] = []
    no_forward_destin: List[str] = []
    administrators: List[Tuple[str, str]] = []
    commands = {}

    def __init__(self, config, botdict: Dict[str, abc_connection]):
        self.botdict = botdict
        self.config = config
        global handler_instance
        if handler_instance is None:
            handler_instance = self
        else:
            raise RuntimeError(
                "There can be only one message handler"
            )
        if 'admins' in config:
            for admin in config['admins']:
                if len(admin) == 2:
                    print(f'Admin: {tuple(admin)}')
                    self.administrators.append(tuple(admin))
        import_submodules(__name__)

    def message_handler(self, msg: message) -> None:
        """
        The message handler. Currently very stupidly relaying
        everything it gets. Should dispatch into other functions/methods
        """
        # print(source + " Message from " + sender + " saying: " + content)
        # I need some source -> destination mapping
        commandreply = False
        command = ""
        if msg.content.startswith('!'):  # ! should modify message forwarding
            # Currently just stupid: set override for all no_forwards
            override = True
        if msg.content.startswith('?'):  # all commands start with ?
            cmd = msg.content.split()[0]
            if cmd in self.commands:
                result = self.commands[cmd].handle(msg)
                # Process result

                # Output (if there is any)
                if not result.silent:
                    commandreply = True
                    command = cmd
        if (
            (not (message.source, message.sender) in self.no_forward_user) or
            (message.source not in self.no_forward_source) or
            override
        ):
            for bot in self.botdict:
                if (
                    bot != msg.source and (
                        bot not in self.no_forward_destin or
                        override
                    )
                ):
                    # Relay Message! (and possibly commandresult)
                    # print("Relay Message from " + source + " to " + bot)
                    self.botdict[bot].post(
                        f"[{msg.source}] {msg.sender} | {msg.content}"
                    )
            if commandreply:
                for bot in self.botdict:
                    if bot not in self.no_forward_destin:
                        if result.isMultiline():
                            for line in result.reply_message.split('\n'):
                                self.botdict[bot].post(
                                    f"[{command}] {line}"
                                )
                        else:
                            self.botdict[bot].post(
                                f"[{command}] {result}"
                            )
