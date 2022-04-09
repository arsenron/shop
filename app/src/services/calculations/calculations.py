from .rules import ICalculationRule, SameKindRule, DiscountRule, ExceedingRule
from src.models.core.cart import ShoppingCart
from src.config import config


class ShoppingCartCalculator:
    def __init__(self, shopping_cart: ShoppingCart):
        self.shopping_cart = shopping_cart

    def select_calculation_rules(self) -> list[ICalculationRule]:
        calculation_rules = []
        if config.calculation_rules.same_kind_rule:
            calculation_rules.append(SameKindRule())
        if config.calculation_rules.discount_rule:
            calculation_rules.append(DiscountRule())
        if config.calculation_rules.exceeding_rule:
            calculation_rules.append(ExceedingRule())
        return calculation_rules

    def calculate_cart(self):
        for calculation_rule in self.select_calculation_rules():
            calculation_rule.apply_rule(self.shopping_cart)
