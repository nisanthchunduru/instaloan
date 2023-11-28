# instaloan

Solution for Demyst's Code Kata https://github.com/DemystData/code-kata

## Demo

Visit https://instaloan.onrender.com for a quick demo

Please note that Render may take 1 - 2 minutes to spin up the website (unless the website has received traffic in the last 15 minutes).

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

### Screenshots

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/b51b6b09-03eb-4e15-ab8c-ccb349c41217)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/d15633b6-b5e2-412b-9cfb-afe74f0b29ce)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/0a718fa2-f480-46df-a76f-011756568118)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/dfaeb222-2e8f-44f8-8e0f-8fc59d58f9c0)

### Todos

- Add an authenticity token to forms
- Add unit tests
- Add integration tests
