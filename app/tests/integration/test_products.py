def test_adding_products(client):
    new_product = {"name": "some-very-unknown-product", "price": 25}
    id = client.put("/products", json=new_product).json()["id"]
    assert client.get(f"/products/{id}").status_code == 200

    product_without_price = {"name": "product-without-price"}
    assert client.put("/products", json=product_without_price).status_code != 200


def test_overwrite_product(client):
    some_very_unknown_product = "some-very-unknown-product"
    new_product_1 = {"name": some_very_unknown_product, "price": 5}
    new_product_2 = {"name": some_very_unknown_product, "price": 10}
    client.put("/products", json=new_product_1)
    client.put("/products", json=new_product_2)

    for product in client.get("/products").json()["products"]:
        if product["name"] == some_very_unknown_product:
            assert product["price"] == 10
            break
    else:
        raise ValueError("could not find product")


def test_delete_product(client):
    new_product = {"name": "product-to-delete", "price": 25}
    id = client.put("/products", json=new_product).json()["id"]

    assert client.delete(f"/products/{id}").status_code == 200

    products = client.get("/products").json()["products"]

    assert any(id != product["id"] for product in products)
