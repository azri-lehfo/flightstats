#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

. venv/bin/activate

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
cd src

if [ -z "$1" ]; then
  worker_name="w1"
else
  worker_name="$1"
fi

if [ -z "$3" ]; then
  log_level="DEBUG"
else
  log_level="$3"
fi

# Check if $2 is provided; if so, add it to the command
if [ -n "$2" ]; then
  command="python -m celery -A flightstats worker -n $worker_name $2 -l $log_level --max-tasks-per-child=10"
else
  command="python -m celery -A flightstats worker -n $worker_name -l $log_level --max-tasks-per-child=10"
fi

# Run the command
eval "$command"
