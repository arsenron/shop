import abc
from fastapi import HTTPException

from abc import abstractmethod
from src.database import Db
from src.deps.common import get_db
from src.deps.cart import get_cart_id
from src.repositories.cart import CartRepository
from fastapi import Depends
from src.models.core.cart import (
    CartProduct,
    AbstractShoppingCart,
    ShoppingCartError,
    ShoppingCart,
)
from .products import IProductService, ProductService
from src.models.schemas.cart import ShoppingCart as ShoppingCartSchema


class ICartService(abc.ABC):
    @abstractmethod
    async def add_product(self, product_id: int) -> int:
        pass

    @abstractmethod
    async def remove_product(self, product_id: int) -> int:
        pass


class CartService:
    def __init__(
        self,
        db: Db = Depends(get_db),
        product_service: IProductService = Depends(ProductService),
        cart_id=Depends(get_cart_id),
    ):
        self.product_service = product_service
        self.cart_repo = CartRepository(db)
        self.cart_id = cart_id

    async def add_product(self, product_id: int, amount: int) -> int:
        cart: AbstractShoppingCart = await self.cart_repo.get_cart(self.cart_id)
        if not cart:
            cart = await self.cart_repo.create_cart(self.cart_id)
        product = await self.product_service.get_product_by_id(product_id)
        cart_product = CartProduct(amount=amount, product=product)
        await self.cart_repo.add_product(cart, cart_product)
        try:
            return cart.calculate_cart()
        except ShoppingCartError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    async def remove_product(self, product_id: int) -> int:
        pass

    async def place_order(self) -> ShoppingCartSchema:
        cart: AbstractShoppingCart = await self.cart_repo.get_cart(self.cart_id)
        if not cart:
            cart = await self.cart_repo.create_cart(self.cart_id)
        try:
            total_amount = cart.calculate_cart()
        except ShoppingCartError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        await self.cart_repo.delete_order(self.cart_id)
        return ShoppingCartSchema(
            total_amount=total_amount, cart_products=cart.cart_products
        )
