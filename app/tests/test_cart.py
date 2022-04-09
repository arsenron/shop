import pytest


def fill_cart(client):
    bread = {"name": "melon", "price": 5}
    melon = {"name": "bread", "price": 10}
    bread_id = client.put("/products", json=bread).json()["id"]
    melon_id = client.put("/products", json=melon).json()["id"]

    assert client.put(f"/cart/add/{bread_id}").status_code == 200
    assert client.put(f"/cart/add/{melon_id}?amount=2").status_code == 200


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


from src.services.calculations.rules import SameKindRule, ExceedingRule, DiscountRule, ShoppingCartError
from src.models.core.cart import ShoppingCart, CartProduct, Product
def test_calculation_strategies():
    shopping_cart = ShoppingCart()
    shopping_cart.add_products([
        CartProduct(amount=5, product=Product(id=2, name="orange", price=4)),
    ])

def test_same_kind_rule():
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(CartProduct(amount=5, product=Product(id=2, name="orange", price=4)))
    same_kind_rule = SameKindRule(every_nth_free_product=5)
    same_kind_rule.apply_rule(shopping_cart)
    assert shopping_cart.total_amount == 16

def test_exceeding_rule():
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(CartProduct(amount=3, product=Product(id=2, name="orange", price=50)))
    with pytest.raises(ShoppingCartError):
        ExceedingRule(maximum_amount=100).apply_rule(shopping_cart)

def test_discount_rule():
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(CartProduct(amount=3, product=Product(id=2, name="orange", price=50)))
    discount_rule = DiscountRule(discount_to_apply=1, total_sum=20)
    discount_rule.apply_rule(shopping_cart)
    assert shopping_cart.total_amount == 149
