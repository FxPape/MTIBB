from nio import AsyncClient, MatrixRoom, RoomMessageText
from time import time
from typing import Callable
import asyncio


class matrix_bot():
    """
        Handles communication with the Matrix homeserver
    """

    def __init__(self, conf, msg_handler: Callable[[str, str, str], None]):
        self.conf = conf
        self.client = AsyncClient(
            conf['homeserver'],
            conf['user']
        )
        self.msg_handler = msg_handler
        self.client.add_event_callback(self.message_callback, RoomMessageText)
        # TODO: Add more callbacks for more RoomMessage-Types here
        print("Matrix setup for " + conf['homeserver'] + " completed")

    async def login(self):
        print(
            await self.client.login(self.conf['password'])
        )
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
        if self.logontime < event.source['origin_server_ts']:
            # print(
            #     f"Message received in room {room.display_name}\n"
            #     f"{room.user_name(event.sender)} | {event.body}"
            # )
            self.msg_handler(
                "Matrix",
                room.user_name(event.sender),
                event.body
            )

    async def astart(self):
        await self.login()
        await self.sync_forever()

    def start(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(self.astart())
