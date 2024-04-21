# instaloan

Instaloan is a prototype Instant Loan service with a beautiful UI

### Screenshots

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/b51b6b09-03eb-4e15-ab8c-ccb349c41217)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/bbaada44-73a3-4b1f-a568-d04c2b8ba2a2)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/e9742075-c23b-4c17-9ab8-d58e9f701020)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/01fd90c8-6d16-4eb9-9d16-0304e686b2cb)

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

### Requirements

See https://github.com/DemystData/code-kata to understand the project's requirements

### Todos

- Investigate splitting the `LoanApplication` model into multiple models
- Add an authenticity token to forms
- Add unit tests
- Add integration tests
