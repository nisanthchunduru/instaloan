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

### Screenshots

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/7445c73d-8aad-412f-9389-82c654036cd2)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/38cfca3c-5dc9-4225-98db-8bf75bc0f7db)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/b5656759-83b3-43e6-bee6-d4d1263bebfb)

![image](https://github.com/nisanthchunduru/instaloan/assets/1789832/c9db33f3-9ab5-4311-be86-d8ad3eaf84d0)

### Todos

- Add form validations to the backend
- Add unit tests
- Add integration tests
