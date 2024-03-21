from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker


class BotMiddleware(BaseMiddleware):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_pre_process_message(self, message, data):
        data['bot'] = self.bot
