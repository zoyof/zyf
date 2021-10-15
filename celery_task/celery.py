from celery import Celery

broker = 'redis://127.0.0.1:6379/1'
backend = 'redis://127.0.0.1:6379/2'
app = Celery(__name__, backend=backend, broker=broker, include=[
    'celery_task.course_task',
    'celery_task.order_task',
    'celery_task.user_task',
])
