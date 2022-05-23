from fastapi import HTTPException, Depends

from src.models.core.products import Product, Products, ProductIn, ProductId
from src.database import Db
from src.deps.common import get_db
from src.repositories.products import ProductRepository, DeletedRowError


class ProductService:
    def __init__(self, db: Db = Depends(get_db)):
        self.product_repo = ProductRepository(db)

    def product_does_not_exist(self) -> HTTPException:
        return HTTPException(status_code=404, detail="product does not exist")

    async def get_products(self) -> Products:
        products_orm = await self.product_repo.get_products()
        return Products(products=[Product.from_orm(po) for po in products_orm])

    async def get_product_by_id(self, id: int) -> Product:
        product = await self.product_repo.get_product_by_id(id)
        if not product:
            raise self.product_does_not_exist()
        else:
            return Product.from_orm(product)

    async def create_or_update_product(self, product_in: ProductIn) -> ProductId:
        product_id = await self.product_repo.add_product(product_in)
        return ProductId(id=product_id)

    async def remove_product(self, id: int):
        try:
            await self.product_repo.remove_product(id)
        except DeletedRowError:
            raise self.product_does_not_exist()

    async def validate_if_product_exists(self, product_id: int):
        await self.get_product_by_id(product_id)
