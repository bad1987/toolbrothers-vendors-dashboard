# Migrations
We are using alembic for migrations
## How to generate migrations and apply them to the database
```
cd migrations
alembic revision --autogenerate -m "a comment here"
alembic upgrade head
```

## Migrate payment method system
localhost:8000/payment/payment-method-system

## Export users cscart in local database
 localhost:8000/admin/cscart-users

 ## Create file Setting.py
 ## add variable SERVER_HOST in this file, create this variable in .env file and give value 'http://localhost:5173'

 # Using SMTP SERVER
 # add variables 
 - SMTP_SERVER_HOST,
 - SMTP_SENDER_MAIL,
 - SMTP_PASSWORD,
 - SMTP_SERVER
 - SMTP_PORT
 # in Setting.py file, create this variable in .env file and give value

 # set these values in seccurity settings

 - API_TOKEN_EXPIRE_DAYS

 # LIST ALL VARIABLE SYSTEM
 # - Connection in MARIA DB local
MARIADB_HOST
MARIADB_PORT
MARIADB_USER
MARIADB_PASSWORD
MARIADB_DB

# - Conection in MARIA DB CS-CART
CSCART_MARIADB_HOST
CSCART_MARIADB_PORT
CSCART_MARIADB_USER
CSCART_MARIADB_PASSWORD
CSCART_MARIADB_DB
# - Server host vue js application
SERVER_HOST

