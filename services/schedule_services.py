from datetime import datetime

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.notify_user import notify


def setup_and_start_schedule(alarm_time, timezone, session, message) -> None:
    scheduler = AsyncIOScheduler(timezone=timezone)
    hour = alarm_time.split(":")[0]
    minute = alarm_time.split(":")[1]

    scheduler.add_job(notify, trigger='cron', hour=hour,
                      minute=minute,
                      start_date=datetime.now(tz=pytz.timezone(timezone)),
                      kwargs={'message': message, 'session': session})

    scheduler.start()
