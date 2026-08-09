from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "trekkify",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.timezone = "Asia/Kolkata"

celery.conf.beat_schedule = {
    "daily-trek-reminders": {
        "task": "application.tasks.send_trek_reminders",
        "schedule": crontab(hour=9, minute=0),
    },
    "monthly-trekking-report": {
        "task": "application.tasks.generate_monthly_report",
        "schedule": crontab(hour=9, minute=5, day_of_month=1),
    },
}

import application.tasks