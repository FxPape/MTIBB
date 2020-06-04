import irc.bot
import irc.strings
from irc.connection import Factory
import ssl
from typing import Callable


class irc_bot(irc.bot.SingleServerIRCBot):
    """
        Handles communication with the IRC server
    """

    def __init__(self, conf, msg_handler: Callable[[str, str, str], None]):
        # self.conf = conf
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
        print("IRC setup for " + conf['host'] + " completed")

    # def on_connect(self, connection, event):
    #    connection.join(self.channel)

    def on_disconnect(self, connection, event):
        print("Disconnected from IRC")
        print(event)

    def on_welcome(self, c, e):
        c.join(self.channel)
        print("IRC join for " + self.host + " completed")

    def on_pubmsg(self, c, e):
        """
            c - connection
            e - event
        e.arguments[0] enthält die Nachricht
        e.source       enthält den Absender
        """
        self.msg_handler("IRC", e.source, e.arguments[0])
