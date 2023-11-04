# MOVIE FAN

## Installation

### Setup Database

Note: Install the latest version of **PostgreSQL** i.e 16

```bash
 sudo su - postgres
 psql
 CREATE DATABASE <movie_fan>;
 CREATE USER <my-user-name> WITH PASSWORD 'password';
 GRANT ALL PRIVILEGES ON DATABASE <movie_fan> TO <my-user-name>;
 \q
```

### Setup Backend
Install **Python 3.9**
```bash
 cd backend
 pip install -r requirements.txt
 
 # create necessary files
 cp .env.sample .env
```

* After setting up above things, change the `.env` file according to your requirements

### Running backend for the first time

```bash
 # load_datasets script will load the movies.csv dataset into databases.
 python manage.py load_datasets
 python manage.py runserver
```

### Setup Frontend

Install: **Nodejs 20.x** and **NPM 10.x**

```bash
 cd frontend
```

Once done, run below commands

```bash
 npm ci
 npm run serve
```

* Now `movie-fan` should be running on `localhost:8080`