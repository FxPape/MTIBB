from aiogram import Bot
from typing import Callable, Dict
from connections import register_type, abc_connection
from helpers import message


@register_type("telegram")
class telegram_bot(abc_connection):
    def __init__(
        self,
        name: str,
        conf: Dict,
        msg_handler: Callable[[message], None]
    ):
        self.name = name
        self.bot = Bot(token=conf['api_token'])
        self.chat_id = conf['chat_id']

    def start(self):
        raise NotImplementedError()

    def post(self, message: str):
        raise NotImplementedError()
