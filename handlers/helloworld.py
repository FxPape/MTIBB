"""
Simple hello world command.
Code to illustrate how commands can be created.
"""
from handlers import (command_handler, command_response, register_command,
                      require_admin)
from helpers import message


@register_command("?hello")
class hello(command_handler):
    hello_count = 0

    def __str__(self):
        return "Greets the sender of the command. Testcommand."

    def handle(self, msg: message):
        self.hello_count = self.hello_count + 1
        return command_response(
            f"Hello {msg.sender}!\nThis is the Hello Nr. " +
            f"{self.hello_count} since start of the Bot."
        )


@register_command("?helloadm")
class helloadm(command_handler):
    hello_count = 0

    def __str__(self):
        return "Greets the sender of the command. Testcommand only for admins."

    @require_admin
    def handle(self, msg: message):
        self.hello_count = self.hello_count + 1
        return command_response(
            f"Hello botadmin {msg.sender}!\nThis is the Hello Nr. " +
            f"{self.hello_count} since start of the Bot."
        )
