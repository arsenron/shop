from abc import ABC, abstractmethod

from pydantic import BaseModel, conint
from src.models.core.products import Product


class ShoppingCartError(Exception):
    pass


class CartProduct(BaseModel):
    amount: conint(ge=1)
    product: Product


class AbstractShoppingCart(BaseModel, ABC):
    cart_products: list[CartProduct]

    def add_product(self, cart_product_to_add: CartProduct) -> int:
        for i, cart_product in enumerate(self.cart_products):
            if cart_product.product.id == cart_product_to_add.product.id:
                self.cart_products[i] = cart_product_to_add
                break
        else:
            self.cart_products.append(cart_product_to_add)

    @abstractmethod
    def calculate_cart(self) -> float:
        pass


class ShoppingCart(AbstractShoppingCart):
    EVERY_NTH_FREE_PRODUCT: int = 5
    TOTAL_SUM_TO_APPLY_DISCOUNT: int = 20
    DISCOUNT_BY_TOTAL_SUM: int = 1
    TOTAL_AVAILABLE_AMOUNT: int = 100

    def calculate_cart(self) -> float:
        """
        :raises ShoppingCartError: when total amount exceeds permitted amount
        """
        total_amount = 0
        for cart_product in self.cart_products:
            number_of_free_products = cart_product.amount // self.EVERY_NTH_FREE_PRODUCT
            total_amount += (
                cart_product.amount - number_of_free_products
            ) * cart_product.product.price
        if total_amount >= self.TOTAL_SUM_TO_APPLY_DISCOUNT:
            total_amount -= self.DISCOUNT_BY_TOTAL_SUM
        if total_amount > self.TOTAL_AVAILABLE_AMOUNT:
            raise ShoppingCartError(
                f"total amount cannot exceed {self.TOTAL_AVAILABLE_AMOUNT}"
            )
        return total_amount
