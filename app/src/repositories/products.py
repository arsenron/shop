from sqlalchemy import select, update

from .base import BaseRepository
from src.models.core.products import ProductIn
from src.models.orm.products import ProductOrm


class DeletedRowError(Exception):
    pass


class ProductRepository(BaseRepository):
    async def get_products(self) -> list[ProductOrm]:
        products = (
            (await self.db.execute(select(ProductOrm).filter(ProductOrm.is_deleted == False))).scalars().all()
        )
        return products

    async def add_product(self, product_in: ProductIn) -> int:
        """
        Updates product in case of matching name

        :returns: product id
        """
        existing_product = await self.db.scalar(select(ProductOrm).filter(ProductOrm.name == product_in.name))
        if existing_product:
            existing_product.price = product_in.price
            existing_product.is_deleted = False
            return existing_product.id
        else:
            product = ProductOrm(name=product_in.name, price=product_in.price)
            self.db.add(product)
            await self.db.flush()
            return product.id

    async def remove_product(self, product_id: int):
        row_is_already_deleted = await self.db.scalar(
            select(ProductOrm)
                .filter(ProductOrm.id == product_id)
                .filter(ProductOrm.is_deleted == True)
                .exists()
                .select()
        )
        if row_is_already_deleted:
            raise DeletedRowError
        else:
            await self.db.execute(
                update(ProductOrm).where(ProductOrm.id == product_id).values(is_deleted=True)
            )

    async def get_product_by_id(self, id: int) -> ProductOrm | None:
        product = await self.db.scalar(select(ProductOrm).filter(ProductOrm.id == id))
        return product
