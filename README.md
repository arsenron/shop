## Shopping API

Simple RESTful API using FastAPI and SQLAlchemy.

### Features

- Ability to create/remove/read products.
- Ability to calculate cart totals without placing an order.
- Ability to customize rules for the cart calculation, for example, defaults are:
    - Every fifth product of same kind is free (order 5 cokes, pay only for 4...);
    - Total amount cannot exceed 100$;
    - Application of a 1$ discount when total amount is 20$ or more


### Prerequisites:
- docker >= 20.10
- docker-compose >= 2

### How to run
- Change dir to: **app**
- Run **./build.sh**
- Run **docker-compose up**
- OpenAPI documentation is accessible through **localhost:9998/docs** endpoint

### How to test
- Change dir to: **app/tests**
- Run **./test.sh**
