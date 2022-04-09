from .commons import BaseModel, RoundedFloat


class ProductIn(BaseModel):
    name: str
    price: float


class ProductId(BaseModel):
    id: int


class Product(BaseModel):
    id: int
    name: str
    price: RoundedFloat


class Products(BaseModel):
    products: list[Product]
