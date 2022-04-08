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
    EVERY_NTH_FREE_PRODUCT: int = 5

    def apply_rule(self, shopping_cart: ShoppingCart):
        for cart_product in shopping_cart.cart_products:
            number_of_free_products = cart_product.amount // self.EVERY_NTH_FREE_PRODUCT
            shopping_cart.total_amount -= number_of_free_products * cart_product.product.price


class DiscountRule(ICalculationRule):
    TOTAL_SUM_TO_APPLY_DISCOUNT: int = 20
    DISCOUNT_BY_TOTAL_SUM: int = 1

    def apply_rule(self, shopping_cart: ShoppingCart):
        if shopping_cart.total_amount > self.TOTAL_SUM_TO_APPLY_DISCOUNT:
            shopping_cart.total_amount -= self.DISCOUNT_BY_TOTAL_SUM


class ExceedingRule(ICalculationRule):
    TOTAL_AVAILABLE_AMOUNT: int = 100

    def apply_rule(self, shopping_cart: ShoppingCart):
        if shopping_cart.total_amount > self.TOTAL_AVAILABLE_AMOUNT:
            raise ShoppingCartError(f"total amount cannot exceed {self.TOTAL_AVAILABLE_AMOUNT}")