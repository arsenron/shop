from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: float


class AllProducts(BaseModel):
    products: list[Product]
