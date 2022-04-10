## Shopping API

Build a RESTful API for a part of a mini shopping app.

### Functional requirements

- Ability to create/remove/read products.
- Ability to calculate cart totals without placing an order.
- Rules for the cart calculation:
	- Every fifth product of same kind is free (order 5 cokes, pay only for 4...);
	- Total amount cannot exceed 100$;
	- Apply a 1$ discount when total amount is 20$ or more

### Technical requirements

- Build a RESTful API (you can choose the technology from Python, Node.js, Java, C# or Go)
- Pay attention to code structure, architecture and API design. Write the code so that it is easy to add more cart calculation rules in the future.
- Use any form of storage to save products & orders.
- Cover the solution with tests.
- Include README with clear instructions on how to build and run your solution.

### Bonus requirements

- Provide OpenAPI documentation
- Use functional programming principles where possible.
- Load cart calculation rules from external storage.


### Prerequisites:
- Linux
- Postgresql >= 10
- Poetry >= 1.1
- Python >= 3.10
- Flyway >= 8

### How to run
- Go to **app** directory and run **poetry install**
- To setup database:
    - Go to **database** directory and try to execute **init.sh** (requires *sudo*)
    - If something bad happens, you may provide your own database credentials in **app/cfg.yaml**
      and apply a database migration to your database located in **database/migrations**. 
- When database is set up, run *shop server* from **app** directory by executing **poetry run app**
- Default port is **9999**, but if it is already used, you can bind to another port by running **poetry run app --bind http://localhost:<your_port>**
- Openapi documentation is accessible through **/docs** endpoint 

### How to test
To run integration tests, configure *postgres* superuser and password. 
By default, they are equal to **postgres** and **postgres**.
To configure, create **DB_SUPERUSER** and **DB_SUPERUSER_PASSWORD** environment variables.

After prerequisistes are met, run **poetry run pytest** from **app** or **app/tests** .
