from datetime import datetime
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.display_tasks import display_scheduled_tasks
from config import SCHEDULE_LIST
from services.user_service import get_all_users


async def repair_all_users_schedule(session, message, bot):
    users = await get_all_users(session)
    for i in users:  # i = [(user_id, timezone, alarm_time, is_active)]
        temp_schedule = Schedule()
        temp_schedule.set_user_settings(timezone=i[1], user_id=i[0])
        temp_schedule.setup_and_start_schedule(alarm_time=i[2], message=message, session=session, bot=bot)
        is_active = i[3]
        if not is_active:
            temp_schedule.scheduler.pause()
        SCHEDULE_LIST[int(i[0])] = temp_schedule
    return True


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

    def setup_and_start_schedule(self, alarm_time, session, message, bot) -> None:
        hour = alarm_time.split(":")[0]
        minute = alarm_time.split(":")[1]

        self.scheduler.add_job(display_scheduled_tasks, trigger='cron', hour=hour,
                               minute=minute, id=str(self.user_id),
                               start_date=datetime.now(tz=pytz.timezone(self.timezone)),
                               kwargs={'message': message, 'session': session, 'job_id': self.user_id, 'bot': bot})
        self.scheduler.start()

    def update_user_schedule(self, alarm_time):
        hour = alarm_time.split(":")[0]
        minute = alarm_time.split(":")[1]
        self.scheduler.reschedule_job(job_id=str(self.user_id), trigger='cron', hour=hour,
                                      minute=minute)
