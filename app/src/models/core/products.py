from .base import BaseModel

class ProductIn(BaseModel):
    name: str
    price: float

class Product(BaseModel):
    id: int
    name: str
    price: float


class AllProducts(BaseModel):
    __root__: list[Product]


class AllProductsSchema(BaseModel):
    products: list[Product]
