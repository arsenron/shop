from commons import BaseModel, RoundedFloat


class ProductIn(BaseModel):
    name: str
    price: float

class Product(BaseModel):
    id: int
    name: str
    price: RoundedFloat


class AllProducts(BaseModel):
    products: list[Product]
