import numbers

from pydantic import BaseModel, validator
from src.models.core.cart import CartProduct


class ShoppingCart(BaseModel):
    total_amount: str
    cart_products: list[CartProduct]

    @validator("total_amount", pre=True)
    def convert_to_usd(cls, value: float) -> str:
        if isinstance(value, numbers.Number):
            return f"{round(value, 1)} $"
        else:
            return value
