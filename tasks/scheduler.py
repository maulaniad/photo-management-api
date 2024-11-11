from celery.schedules import crontab


BEAT_SCHEDULE = {
    "hello": {
        "task": "tasks.task_hello.task_say_hello",
        "schedule": crontab(hour="*", minute=0),
    },
}
