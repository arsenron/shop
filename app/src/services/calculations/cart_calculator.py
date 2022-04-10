from .rules import ICalculationRule
from src.models.core.cart import ShoppingCart
from src.config import config


class ShoppingCartCalculator:
    def __init__(self, shopping_cart: ShoppingCart):
        self.shopping_cart = shopping_cart

    def apply_calculation_rules(self):
        rule: ICalculationRule | None
        for _, rule in config.calculation_rules:
            if rule:
                rule.apply_rule(self.shopping_cart)
