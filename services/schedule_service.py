from datetime import datetime
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.get_tasks import get_all_user_tasks


class Schedule:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.timezone = None
        self.user_id = None

    def set_user_settings(self, timezone, user_id):
        if not self.timezone and not self.user_id:
            self.scheduler.timezone = pytz.timezone(timezone)
            self.user_id = user_id
            self.timezone = timezone
        else:
            pass

    def setup_and_start_schedule(self, alarm_time, session, message) -> None:
        hour = alarm_time.split(":")[0]
        minute = alarm_time.split(":")[1]

        self.scheduler.add_job(get_all_user_tasks, trigger='cron', hour=hour,
                               minute=minute, id=str(self.user_id),
                               start_date=datetime.now(tz=pytz.timezone(self.timezone)),
                               kwargs={'message': message, 'session': session})

        self.scheduler.start()

    def update_user_schedule(self, alarm_time):
        hour = alarm_time.split(":")[0]
        minute = alarm_time.split(":")[1]
        self.scheduler.reschedule_job(job_id=str(self.user_id), trigger='cron', hour=hour,
                                      minute=minute)
