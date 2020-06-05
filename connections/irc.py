import irc.bot
import irc.strings
from irc.connection import Factory
import ssl
from typing import Callable, Dict
from connections import register_type, abc_connection


@register_type("irc")
class irc_bot(irc.bot.SingleServerIRCBot, abc_connection):
    """
    Handles communication with a IRC server
    """

    def __init__(
        self,
        name: str,
        conf: Dict,
        msg_handler: Callable[[str, str, str], None]
    ):
        self.name = name
        self.nickname = conf['nick']
        self.channel = conf['channel']
        self.host = conf['host']
        irc.bot.SingleServerIRCBot.__init__(
            self,
            [(conf['host'], conf['port'])],
            self.nickname,
            self.nickname,
            connect_factory=Factory(wrapper=ssl.wrap_socket)
        )
        self.msg_handler = msg_handler
        # print("IRC setup for " + conf['host'] + " completed")

    # def on_connect(self, connection, event):
    #    connection.join(self.channel)

    def on_disconnect(self, connection, event):
        print("Disconnected from IRC")
        print(event)

    def on_welcome(self, client, event):
        client.join(self.channel)
        print("IRC join for " + self.host + " completed")

    def on_pubmsg(self, client, event):
        """
        Callback for recieving messages from the server
        """
        sender = event.source.split('!')[0]
        if sender != self.nickname:
            self.msg_handler(self.name, sender, event.arguments[0])

    def post(self, message: str) -> None:
        # self.connection.notice(self.channel, message)
        self.connection.privmsg(self.channel, message)
