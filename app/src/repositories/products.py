from sqlalchemy import select, update

from .base import BaseRepository
from src.models.core.products import Products, Product, ProductIn
from src.models import orm
import src.models.orm.products


class ProductRepository(BaseRepository):
    async def get_products(self) -> Products:
        products_orm = (
            await self.db.execute(
                select(orm.products.Products).filter(orm.products.Products.is_deleted == False)
            )
        ).all()
        list_of_product_models = [row[0] for row in products_orm]
        return Products(products=[Product.from_orm(m) for m in list_of_product_models])

    async def add_product(self, product_in: ProductIn) -> int:
        """
        Updates product in case of matching name

        :returns: product id
        """
        existing_product = await self.db.scalar(
            select(orm.products.Products).filter(orm.products.Products.name == product_in.name)
        )
        if existing_product:
            existing_product.price = product_in.price
            existing_product.is_deleted = False
            return existing_product.id
        else:
            product = orm.products.Products(name=product_in.name, price=product_in.price)
            self.db.add(product)
            await self.db.flush()
            return product.id

    async def remove_product(self, product_id: int):
        await self.db.execute(
            update(orm.products.Products)
            .where(orm.products.Products.id == product_id)
            .values(is_deleted=True)
        )

    async def get_product_by_id(self, id: int) -> Product | None:
        product_orm = await self.db.scalar(
            select(orm.products.Products).filter(orm.products.Products.id == id)
        )
        if product_orm:
            return Product.from_orm(product_orm)
        else:
            return None
