from typing import Callable, Awaitable, Dict, Any

from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def on_pre_process_message(self, message, data):
        data['session'] = self.session_pool
