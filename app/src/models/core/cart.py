from pydantic import BaseModel, conint
from src.models.core.products import Product


class CartProduct(BaseModel):
    amount: conint(ge=1)
    product: Product


class ShoppingCart(BaseModel):
    total_amount: int
    products: list[CartProduct]

    def add_product(self, cart_product_to_add: CartProduct) -> int:
        # for cart_product in self.products:
        #     if cart_product.product.id == cart_product_to_add.product.id:
        #
        self.products.append(cart_product_to_add)
        self.total_amount += cart_product_to_add.product.price * cart_product_to_add.amount
        return self.total_amount
