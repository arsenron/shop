from pydantic import conint
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

    def add_product(self, cart_product: CartProduct) -> int:
        cost_of_products = cart_product.product.price * cart_product.amount
        for i, existing_cart_product in enumerate(self.cart_products):
            if existing_cart_product.product.id == cart_product.product.id:
                self.cart_products[i] = cart_product
                self.total_amount += cost_of_products
                break
        else:
            self.cart_products.append(cart_product)
            self.total_amount += cost_of_products
