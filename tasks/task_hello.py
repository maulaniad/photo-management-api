from celery import Task, shared_task


Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls) # type: ignore[attr-defined]

@shared_task(bind=True, ignore_result=True)
def task_say_hello(self: Task):
    self.update_state(state="RUNNING", meta={})
    print("Hello from Celery")
    self.update_state(state="SUCCESS", meta={})
    return True
