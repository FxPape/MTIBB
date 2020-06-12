"""
Commands to modify the message forwarding
"""

from handlers import command_handler, command_response, register_command
from helpers import message


@register_command("?muteme")
class muteme(command_handler):
    def __str__(self):
        return (
            "Disables relaying messages from the calling user." +
            " Prefixing a message with ! will still forward"
        )

    def handle(self, msg: message):
        if (msg.source, msg.sender) in self.message_handler.no_forward_user:
            return command_response(
                "You're already bridge-muted."
            )
        else:
            self.message_handler.no_forward_user.append(
                (msg.source, msg.sender)
            )
            return command_response(
                "You will no longer be forwarded."
            )


@register_command("?relayme")
class relayme(command_handler):
    def __str__(self):
        return "Enables relaying of all messages from the calling user"

    def handle(self, msg: message):
        if (msg.source, msg.sender) in self.message_handler.no_forward_user:
            self.message_handler.no_forward_user.remove(
                (msg.source, msg.sender)
            )
            return command_response(
                "Forwarding enabled"
            )
        else:
            return command_response(
                "You are already being forwarded"
            )
