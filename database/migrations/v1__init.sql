DROP TABLE products CASCADE;
CREATE TABLE products
(
    id    SERIAL PRIMARY KEY,
    name  text NOT NULL UNIQUE,
    price real NOT NULL
);


CREATE TABLE carts
(
    id         text PRIMARY KEY,
    created_at timestamp NOT NULL DEFAULT now()
);


CREATE TABLE cart_products
(
    id         SERIAL PRIMARY KEY,
    cart_id    text NOT NULL REFERENCES carts (id),
    product_id int  NOT NULL REFERENCES products (id),
    amount     int  NOT NULL DEFAULT 1,
    is_placed  bool NOT NULL DEFAULT false,
    UNIQUE (cart_id, product_id)
);


INSERT INTO products  -- default products
VALUES (1, 'banana', 1.5),
       (2, 'orange', 0.5),
       (3, 'watermelon', 4),
       (4, 'bread', 0.3),
       (5, 'milk', 1),
       (6, 'sugar', 2);
