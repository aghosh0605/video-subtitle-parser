import time
from celery_progress.backend import ProgressRecorder
from celery import shared_task 

@shared_task(bind=True)
def wait_sometime_one(self, seconds):
    progress_recorder = ProgressRecorder(self)
    result = 0
    for i in range(seconds):
        time.sleep(5)
        result += i
        progress_recorder.set_progress(i + 1, seconds,f'Sleep Progress Track')
    return result