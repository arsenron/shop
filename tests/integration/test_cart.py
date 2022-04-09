def fill_cart(client):
    bread = {"name": "melon", "price": 5}
    melon = {"name": "bread", "price": 10}
    bread_id = client.put("/products", json=bread).json()["id"]
    melon_id = client.put("/products", json=melon).json()["id"]

    assert client.put(f"/cart/add/{bread_id}").status_code == 200
    assert client.put(f"/cart/add/{melon_id}?amount=2").status_code == 200

    return bread_id, melon_id


def test_cart(client):
    fill_cart(client)

    shopping_cart = client.post("/cart/place").json()
    products = sorted(shopping_cart["cart_products"], key=lambda p: p["product"]["name"])
    match products:
        case [
            {"amount": 2, "product": {"name": "bread"}},
            {"amount": 1, "product": {"name": "melon"}},
        ]:
            pass
        case _:
            raise ValueError("shopping cart does not match")

def test_cart_is_empty_after_it_is_placed(client):
    shopping_cart = client.post("/cart/place").json()
    assert shopping_cart["cart_products"] == []

    fill_cart(client)

    shopping_cart = client.post("/cart/place").json()
    assert shopping_cart["cart_products"] != []

    shopping_cart = client.post("/cart/place").json()
    assert shopping_cart["cart_products"] == []


def test_remove_from_cart(client):
    bread_id, melon_id = fill_cart(client)

    client.put(f"/cart/add/{bread_id}?amount=0")
    total_amount = client.put(f"/cart/add/{melon_id}?amount=0").json()["total_amount"]
    assert total_amount == 0
