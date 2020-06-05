from nio import AsyncClient, MatrixRoom, RoomMessageText
from time import time
from typing import Callable, Dict
import asyncio
from connections import register_type, abc_connection


@register_type("matrix")
class matrix_bot(abc_connection):
    """
    Handles communication with a Matrix homeserver
    """

    def __init__(
        self,
        name: str,
        conf: Dict,
        msg_handler: Callable[[str, str, str], None]
    ):
        self.name = name
        self.conf = conf
        self.client = AsyncClient(
            conf['homeserver'],
            conf['user']
        )
        self.msg_handler = msg_handler
        self.client.add_event_callback(self.message_callback, RoomMessageText)
        # TODO: Add more callbacks for more RoomMessage-Types here
        # print("Matrix setup for " + conf['homeserver'] + " completed")

    async def login(self):
        await self.client.login(self.conf['password'])
        # reply = await self.client.login(self.conf['password'])
        # print(reply)

        # await self.client.room_send(
        #     room_id=self.conf['room'],
        #     message_type="m.room.message",
        #     content={
        #         "msgtype": "m.text",
        #         "body": "Bot online!"
        #     }
        # )
        self.logontime = time() * 1000
        print("Matrix login for " + self.conf['homeserver'] + " completed")

    async def sync_forever(self, timeout=15000):
        await self.client.sync_forever(timeout)

    async def message_callback(
        self,
        room: MatrixRoom,
        event: RoomMessageText
    ) -> None:
        if (
            self.logontime < event.source['origin_server_ts'] and
            room.user_name(event.sender) != self.nick
        ):
            self.msg_handler(
                self.name,
                room.user_name(event.sender),
                event.body
            )

    async def astart(self):
        await self.login()
        nick = await self.client.get_displayname()
        # nick includes a leading "Display Name: "
        # Strip that:
        self.nick = str(nick)[14:]
        # Note: this could produce problems if not display name is set
        # But every bot should in theory have one
        await self.sync_forever()

    def start(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        asyncio.get_event_loop().run_until_complete(self.astart())

    async def apost(self, message):
        await self.client.room_send(
            room_id=self.conf['room'],
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message
            }
        )

    def post(self, message: str) -> None:
        try:
            prev = asyncio.get_event_loop()
        except RuntimeError:
            prev = None
        asyncio.set_event_loop(self.loop)
        asyncio.get_event_loop().create_task(self.apost(message))
        asyncio.set_event_loop(prev)
