import pytest

from src.services.calculations.rules import (
    SameKindRule,
    ExceedingRule,
    DiscountRule,
    ShoppingCartError,
)
from src.models.core.cart import ShoppingCart, CartProduct, Product


def test_shopping_cart_total_amount():
    shopping_cart = ShoppingCart()
    shopping_cart.add_products(
        [
            CartProduct(amount=5, product=Product(id=2, name="orange", price=5)),
            CartProduct(amount=10, product=Product(id=2, name="orange", price=3)),
            CartProduct(amount=3, product=Product(id=2, name="orange", price=1)),
        ]
    )
    assert shopping_cart.total_amount == 58


def test_same_kind_rule():
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(
        CartProduct(amount=5, product=Product(id=2, name="orange", price=4))
    )
    same_kind_rule = SameKindRule(free_product=5)
    same_kind_rule.apply_rule(shopping_cart)
    assert shopping_cart.total_amount == 16


def test_exceeding_rule():
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(
        CartProduct(amount=3, product=Product(id=2, name="orange", price=50))
    )
    with pytest.raises(ShoppingCartError):
        ExceedingRule(total_sum=100).apply_rule(shopping_cart)


def test_discount_rule():
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(
        CartProduct(amount=3, product=Product(id=2, name="orange", price=50))
    )
    discount_rule = DiscountRule(discount_to_apply=1, total_sum=20)
    discount_rule.apply_rule(shopping_cart)
    assert shopping_cart.total_amount == 149

    shopping_cart = ShoppingCart()
    shopping_cart.add_product(
        CartProduct(amount=3, product=Product(id=2, name="orange", price=6))
    )
    discount_rule = DiscountRule(discount_to_apply=1, total_sum=20)
    discount_rule.apply_rule(shopping_cart)
    assert shopping_cart.total_amount == 18
