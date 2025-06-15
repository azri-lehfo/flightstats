# flightstats

flightstats scraping

---

## Requirements

- Python: 3.13.0
- Django: 5.2

### Configure editor

1. Set convert tabs to spaces with indent using 4 spaces.
2. Set max line length to 120.
3. Set ensure newline at end of file on save.
4. Set trim trailing white space on save.

### Best practice

1. Single quotes for data, double quotes for human-readable strings.
2. To comply with certain strict accounting or financial regulations, please use `max_digits=19` and `decimal_places=4` on money related field, see more in this [StackOverflow](https://stackoverflow.com/questions/224462/storing-money-in-a-decimal-column-what-precision-and-scale/224866#224866) answer

---

## Setup in local

### To setup pyenv

1. Install Python 3.13.0.
   ```sh
   $ pyenv install 3.13.0
   ```
2. Install virtualenv **flightstats**.
   ```sh
   $ pyenv virtualenv 3.13.0 flightstats
   ```
3. Install requirements.
   ```sh
   $ pip install -r requirements.txt
   ```

### Setup database in PostgreSQL

1. Access to PostgreSQL in terminal.
   ```sh
   $ psql postgres
   ```
2. Run SQL to create user **flightstats** and database **flightstats**.
   ```sql
   CREATE ROLE flightstats WITH LOGIN PASSWORD 'flightstats';
   ALTER ROLE flightstats CREATEDB;
   CREATE DATABASE flightstats;
   GRANT ALL PRIVILEGES ON DATABASE flightstats TO flightstats;
   ```

### Setup Redis and RabbitMQ

1. Install Redis
   ```sh
   $ brew install redis
   ```

2. Install RabbitMQ
   ```sh
   $ brew install rabbitmq
   ```

3. Make sure the services are running
   ```sh
   $ brew services
   ```
   You should have below services running:
   ```sh
   postgresql@14 started <owner> /Users/<owner>/Library/LaunchAgents/homebrew.mxcl.postgresql@14.plist
   rabbitmq      started <owner> /Users/<owner>/Library/LaunchAgents/homebrew.mxcl.rabbitmq.plist
   redis         started <owner> /Users/<owner>/Library/LaunchAgents/homebrew.mxcl.redis.plist
   ```
   If not, please run:
   ```sh
   $ brew services start postgresql@14
   $ brew services start rabbitmq
   $ brew services start redis
   ```

### Setup project for first time

1. Run Celery.
   ```sh
   $ cd ./src
   # Queued async tasks
   $ celery -A flightstats worker -l DEBUG
   # Periodic tasks
   $ celery -A flightstats beat -l DEBUG
   ```

2. Install Python libraries.
   ```sh
   $ pip install --upgrade pip
   $ pip install -r ./requirements.txt
   ```

3. Migrate and runserver.
   ```sh
   $ ./manage.py migrate
   $ ./manage.py runserver
   ```

4. Access to http://localhost:8000/api/flight-service/flights/?airline=aa&flight_number=100&departure_date=06-06-15

---

### To run test cases
```sh
$ coverage run ./src/manage.py test src -v 2 --parallel && coverage report -m
```

---

## Follow [The Twelve Factors](https://12factor.net/) methodology

#### I. Codebase
> One codebase tracked in revision control, many deploys

#### II. Dependencies
> Explicitly declare and isolate dependencies

#### III. Config
> Store config in the environment

#### IV. Backing services
> Treat backing services as attached resources

#### V. Build, release, run
> Strictly separate build and run stages

#### VI. Processes
> Execute the app as one or more stateless processes

#### VII. Port binding
> Export services via port binding

#### VIII. Concurrency
> Scale out via the process model

#### IX. Disposability
> Maximize robustness with fast startup and graceful shutdown

#### X. Dev/prod parity
> Keep development, staging, and production as similar as possible

#### XI. Logs
> Treat logs as event streams

#### XII. Admin processes
> Run admin/management tasks as one-off processes
