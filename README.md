# instaloan

Solution for Demyst's Code Kata https://github.com/DemystData/code-kata

## Installation

Install dependencies

```
pip install -r requirements.txt
```

Start Postgres

```
docker compose up
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
