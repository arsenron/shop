CREATE TABLE products
(
    id    SERIAL PRIMARY KEY,
    name  text NOT NULL UNIQUE,
    price real NOT NULL,
    is_deleted bool DEFAULT false
);


CREATE TABLE carts
(
    id         SERIAL PRIMARY KEY ,
    session_id text NOT NULL ,
    created_at timestamp NOT NULL DEFAULT now(),
    is_placed  bool NOT NULL DEFAULT false
);

CREATE UNIQUE INDEX ON carts (session_id, is_placed) WHERE is_placed = false;


CREATE TABLE cart_products
(
    id         SERIAL PRIMARY KEY,
    carts_id    int NOT NULL REFERENCES carts (id),
    product_id int  NOT NULL REFERENCES products (id),
    amount     int  NOT NULL DEFAULT 1,
    UNIQUE (carts_id, product_id)
);

INSERT INTO products (name, price)
VALUES ('banana', 1.5),
       ('orange', 0.5),
       ('watermelon', 4),
       ('bread', 0.3),
       ('milk', 1),
       ('sugar', 2);
