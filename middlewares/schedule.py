
from aiogram.dispatcher.middlewares import BaseMiddleware

from services.schedule_service import Schedule


class ScheduleMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.schedule = Schedule()

    async def on_pre_process_message(self, message, data):
        data['schedule'] = self.schedule
