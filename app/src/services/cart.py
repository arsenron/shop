import abc
from fastapi import HTTPException

from src.models.core.products import AllProducts, Product
from abc import abstractmethod
from src.database import Db
from src.deps.common import get_db
from src.repositories.products import ProductRepository
from src.repositories.cart import CartRepository
from fastapi import Depends
from src.lib import default_response
from src.models.core.cart import CartProduct
from .products import IProductService, ProductService


class ICartService(abc.ABC):
    @abstractmethod
    async def add_product(self, product_id: int) -> int:
        pass

    @abstractmethod
    async def remove_product(self, product_id: int) -> int:
        pass


class CartService:
    def __init__(self,
        db: Db = Depends(get_db),
        product_service: IProductService = Depends(ProductService)
    ):
        self.product_service = product_service
        self.cart_repo = CartRepository(db)
        self.cart_id = "DEFAULT"

    async def add_product(self, product_id: int, amount: int) -> int:
        cart = await self.cart_repo.get_cart(self.cart_id)
        if not cart:
            cart = await self.cart_repo.create_cart(self.cart_id)
        product = await self.product_service.get_product_by_id(product_id)
        cart_product = CartProduct(amount=amount, product=product)
        await self.cart_repo.add_product(cart, cart_product)
        return cart.total_amount

    async def remove_product(self, product_id: int) -> int:
        pass


