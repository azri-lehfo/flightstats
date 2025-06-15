#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

. venv/bin/activate

cd src
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
# python -m celery beat -A flightstats.celery -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
python -m celery -A flightstats beat --scheduler django_celery_beat.schedulers:DatabaseScheduler -l DEBUG
