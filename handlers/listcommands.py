"""
Commands to list stuff
"""

from handlers import (command_handler, command_response, register_command,
                      register_commands)
from helpers import message


@register_commands(["?help", "?listcmd"])
class listcmd(command_handler):
    def __str__(self):
        return "Lists all commands and their description"

    def handle(self, msg: message):
        output = 'List of all commands known to this bot:'
        commands = self.message_handler.commands
        for cmd in sorted(commands.keys()):
            output = (
                output +
                f"\n {cmd} - {str(commands[cmd])}"
            )
        return command_response(
            output
        )


@register_command("?listchannels")
class listchannels(command_handler):
    def __str__(self):
        return "Lists all channels the bot is connected to"

    def handle(self, msg: message):
        output = 'List of all channels of this bot:'
        botdict = self.message_handler.botdict
        for bot in botdict:
            output = (
                output +
                f'\n ({bot}) - {str(botdict[bot])}'
            )
        return command_response(
            output
        )
