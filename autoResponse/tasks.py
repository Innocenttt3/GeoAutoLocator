from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task()
def countdown(start):
    for i in range(start, -1, -1):
        print(i)