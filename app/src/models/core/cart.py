from pydantic import conint, root_validator

from .commons import BaseModel, RoundedFloat
from src.models.core.products import Product


class TotalAmount(BaseModel):
    total_amount: RoundedFloat


class CartProduct(BaseModel):
    amount: conint(ge=0)
    product: Product


class ShoppingCart(BaseModel):
    cart_products: list[CartProduct] = []
    total_amount: RoundedFloat = 0

    @root_validator
    def calculate_cart(cls, values):
        total_amount = 0
        cart_products = values["cart_products"]
        if cart_products:
            for i, cart_product in enumerate(cart_products):
                cost_of_products = cart_product.product.price * cart_product.amount
                total_amount += cost_of_products
        values["total_amount"] = total_amount
        return values
