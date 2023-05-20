
from celery import shared_task
import time

@shared_task
def sleep_sometime():
    time.sleep(20)
    print('Recharge Done')