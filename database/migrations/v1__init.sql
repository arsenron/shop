CREATE TABLE products(
    id int PRIMARY KEY,
    name text NOT NULL UNIQUE ,
    price real NOT NULL
);


CREATE TABLE carts(
    id text PRIMARY KEY ,
    created_at timestamp NOT NULL DEFAULT now()
);


CREATE TABLE cart_products(
    id SERIAL PRIMARY KEY ,
    cart_id text NOT NULL REFERENCES carts(id),
    product_id int NOT NULL REFERENCES products(id),
    amount int NOT NULL DEFAULT 1,
    is_placed bool NOT NULL DEFAULT false,
    UNIQUE (cart_id, product_id)
);
