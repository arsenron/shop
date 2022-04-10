from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.models.core.cart import ShoppingCart


class ShoppingCartError(Exception):
    pass


class ICalculationRule(ABC):
    @abstractmethod
    def apply_rule(self, shopping_cart: ShoppingCart):
        """
        :raise ShoppingCartError: In case of invalid requirements
        """
        pass


class SameKindRule(ICalculationRule, BaseModel):
    free_product: int = 5

    def apply_rule(self, shopping_cart: ShoppingCart):
        for cart_product in shopping_cart.cart_products:
            number_of_free_products = cart_product.amount // self.free_product
            shopping_cart.total_amount -= (
                number_of_free_products * cart_product.product.price
            )


class DiscountRule(ICalculationRule, BaseModel):
    discount_amount = 1
    total_sum = 20

    def apply_rule(self, shopping_cart: ShoppingCart):
        if shopping_cart.total_amount > self.total_sum:
            shopping_cart.total_amount -= self.discount_amount


class ExceedingRule(ICalculationRule, BaseModel):
    total_sum: int = 100

    def apply_rule(self, shopping_cart: ShoppingCart):
        if shopping_cart.total_amount > self.total_sum:
            raise ShoppingCartError(f"total amount cannot exceed {self.total_sum}")
