from abc import ABC, abstractmethod

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


class SameKindRule(ICalculationRule):
    def __init__(self, every_nth_free_product: int = 5):
        self.every_nth_free_product = every_nth_free_product

    def apply_rule(self, shopping_cart: ShoppingCart):
        for cart_product in shopping_cart.cart_products:
            number_of_free_products = cart_product.amount // self.every_nth_free_product
            shopping_cart.total_amount -= (
                number_of_free_products * cart_product.product.price
            )


class DiscountRule(ICalculationRule):
    def __init__(self, discount_to_apply: int = 1, total_sum: int = 20):
        self.discount_to_apply = discount_to_apply
        self.total_sum = total_sum

    def apply_rule(self, shopping_cart: ShoppingCart):
        if shopping_cart.total_amount > self.total_sum:
            shopping_cart.total_amount -= self.discount_to_apply


class ExceedingRule(ICalculationRule):
    def __init__(self, maximum_amount: int = 100):
        self.maximum_amount = maximum_amount

    def apply_rule(self, shopping_cart: ShoppingCart):
        if shopping_cart.total_amount > self.maximum_amount:
            raise ShoppingCartError(f"total amount cannot exceed {self.maximum_amount}")
