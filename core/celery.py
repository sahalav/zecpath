from celery import Celery

app = Celery('core')

app.conf.broker_url = 'redis://localhost:6379/0'