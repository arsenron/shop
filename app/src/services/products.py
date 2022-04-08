import abc
from fastapi import HTTPException

from src.models.core.products import AllProducts, Product
from abc import abstractmethod
from src.database import Db
from src.deps.common import get_db
from src.repositories.products import ProductRepository
from fastapi import Depends
from src.lib import default_response


class IProductService(abc.ABC):
    @abstractmethod
    async def get_products(self) -> AllProducts:
        pass

    @abstractmethod
    async def get_product_by_id(self, id: int) -> Product:
        pass

    @abstractmethod
    async def create_product(self, product: Product):
        pass

    @abstractmethod
    async def remove_product(self, id: int):
        pass


class ProductService(IProductService):
    def __init__(self, db: Db = Depends(get_db)):
        self.product_repo = ProductRepository(db)

    async def get_products(self) -> AllProducts:
        return await self.product_repo.get_products()

    async def get_product_by_id(self, id: int) -> Product:
        product = await self.product_repo.get_product_by_id(id)
        if not product:
            raise HTTPException(status_code=400, detail="product does not exist")
        else:
            return product

    async def create_product(self, product: Product):
        await self.product_repo.add_product(product)

    async def remove_product(self, id: int):
        await self.product_repo.remove_product(id)
        return default_response
