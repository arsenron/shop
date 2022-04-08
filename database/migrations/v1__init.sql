DROP TABLE cart_products;
DROP TABLE carts;
DROP TABLE products CASCADE;

CREATE TABLE products
(
    id    SERIAL PRIMARY KEY,
    name  text NOT NULL UNIQUE,
    price real NOT NULL
);


CREATE TABLE carts
(
    id         SERIAL PRIMARY KEY ,
    cart_id text NOT NULL ,
    created_at timestamp NOT NULL DEFAULT now(),
    is_placed  bool NOT NULL DEFAULT false
);

CREATE UNIQUE INDEX ON carts (cart_id, is_placed) WHERE is_placed = false;


CREATE TABLE cart_products
(
    id         SERIAL PRIMARY KEY,
    carts_id    int NOT NULL REFERENCES carts (id),
    product_id int  NOT NULL REFERENCES products (id),
    amount     int  NOT NULL DEFAULT 1,
    UNIQUE (carts_id, product_id)
);


INSERT INTO products (name, price)  -- default products
VALUES ('banana', 1.5),
       ('orange', 0.5),
       ('watermelon', 4),
       ('bread', 0.3),
       ('milk', 1),
       ('sugar', 2);

