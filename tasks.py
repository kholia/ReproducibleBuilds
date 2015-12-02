from celery import Celery
import worker

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'

BROKER_URL = 'redis://localhost:6379/0'
celery = Celery('tasks', backend='redis://', broker=BROKER_URL)

@celery.task
def process_build(id):
    return worker.process_build(id)
