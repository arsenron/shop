from abc import ABC, abstractmethod

from .rules import ICalculationRule, SameKindRule, DiscountRule, ExceedingRule
from src.models.core.cart import ShoppingCart


class AbstractShoppingCartCalculator(ABC):
    def __init__(self, shopping_cart: ShoppingCart):
        self.shopping_cart = shopping_cart

    @abstractmethod
    def select_calculation_rules(self) -> list[ICalculationRule]:
        pass

    def calculate_cart(self) -> float:
        for calculation_rule in self.select_calculation_rules():
            calculation_rule.apply_rule(self.shopping_cart)
        return self.shopping_cart.total_amount


class ShoppingCartCalculator(AbstractShoppingCartCalculator):
    def select_calculation_rules(self) -> list[ICalculationRule]:
        return [SameKindRule(), DiscountRule(), ExceedingRule()]