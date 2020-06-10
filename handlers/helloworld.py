from handlers import command_handler, command_response, register_command
from helpers import message


@register_command("?hello")
class helloworld(command_handler):
    def handle(self, msg: message):
        return command_response(f"Hello {msg.sender}!")
