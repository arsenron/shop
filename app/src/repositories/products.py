from .base import BaseRepository
from src.models.schemas.products import AllProducts, Product


products = AllProducts(
    products=[
        Product(id=1, name="banana", price=1.5),
        Product(id=2, name="apple", price=0.5),
        Product(id=3, name="orange", price=2.3),
        Product(id=4, name="watermelon", price=5),
    ]
)


class ProductRepository(BaseRepository):
    async def get_products(self) -> AllProducts:
        return products

    async def add_product(self, product_to_add: Product):
        for id, product_in_db in enumerate(products.products):
            if product_to_add.id == product_in_db.id:
                products.products[id] = product_to_add
                break
        else:
            products.products.append(product_to_add)

    async def remove_product(self, product_id: int):
        for i, p in enumerate(products.products):
            if p.id == product_id:
                del products.products[i]

    async def get_product_by_id(self, id: int) -> Product | None:
        for p in products.products:
            if p.id == id:
                return p
