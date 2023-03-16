# Migrations
We are using alembic for migrations
## How to generate migrations and apply them to the database
```
cd migrations
alembic revision --autogenerate -m "a comment here"
alembic upgrade head
```