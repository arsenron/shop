from sqlalchemy import select, delete

from .base import BaseRepository
from src.models.core.products import AllProducts, Product, ProductIn
from src.models.orm.products import Products as ProductsORM


class ProductRepository(BaseRepository):
    async def get_products(self) -> AllProducts:
        product_models = (await self.db.execute(
            select(ProductsORM)
        )).all()
        list_of_product_models = [row[0] for row in product_models]
        return AllProducts(products=[Product.from_orm(m) for m in list_of_product_models])

    async def add_product(self, product_in: ProductIn):
        """
        Updates product in case of matching name
        """
        existing_product = await self.db.scalar(
            select(ProductsORM).filter(ProductsORM.name == product_in.name)
        )
        if existing_product:
            existing_product.price = product_in.price
        else:
            product = ProductsORM(name=product_in.name, price=product_in.price)
            self.db.add(product)

    async def remove_product(self, product_id: int):
        await self.db.execute(
            delete(ProductsORM).where(ProductsORM.id == product_id)
        )

    async def get_product_by_id(self, id: int) -> Product | None:
        product_orm = await self.db.scalar(
            select(ProductsORM).filter(ProductsORM.id == id)
        )
        if product_orm:
            return Product.from_orm(product_orm)
        else:
            return None

    async def check_if_product_exists(self, id: int) -> Product | None:
        return await self.db.scalar(
            select(1).filter(ProductsORM.id == id).exists().select()
        )
