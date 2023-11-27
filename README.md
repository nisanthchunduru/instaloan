# instaloan

Solution for Demyst's Code Kata https://github.com/DemystData/code-kata

## Demo

Visit https://instaloan.onrender.com for a quick demo

## Installation

Start the app

```
docker compose up --build
```

and visit http://localhost:8080

If you don't want to start the app in Docker, follow the steps below.

Install dependencies

```
pip install -r requirements.txt
```

Start Postgres

```
docker compose up postgres
```

Create the database

```
psql -h localhost -U postgres -a -f create_db.sql
```

Run migrations

```
flask db upgrade
```

Start the app

```
python app.py
```
