from nio import AsyncClient, MatrixRoom, RoomMessageText
from time import time


class matrix_bot():
    """
        Handles communication with the Matrix homeserver
    """

    def __init__(self, conf):
        self.conf = conf
        self.client = AsyncClient(
            conf['homeserver'],
            conf['user']
        )
        self.client.add_event_callback(self.message_callback, RoomMessageText)

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

    async def sync_forever(self, timeout=15000):
        await self.client.sync_forever(timeout)

    async def message_callback(
        self,
        room: MatrixRoom,
        event: RoomMessageText
    ) -> None:
        if self.logontime < event.source['origin_server_ts']:
            print(
                f"Message received in room {room.display_name}\n"
                f"{room.user_name(event.sender)} | {event.body}"
            )
