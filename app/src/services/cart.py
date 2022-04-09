from abc import abstractmethod, ABC

from fastapi import HTTPException
from fastapi import Depends

from src.database import Db
from src.deps.common import get_db
from src.deps.cart import get_cart_id
from src.repositories.cart import CartRepository
from src.models.core.cart import (
    CartProduct,
    ShoppingCart,
    TotalAmount
)
from src.models import orm
import src.models.orm.cart
from .calculations.calculations import ShoppingCartCalculator
from .calculations.rules import ShoppingCartError
from .products import ProductService


class ICartService(ABC):
    @abstractmethod
    async def add_product(self, product_id: int, amount: int) -> TotalAmount:
        pass

    @abstractmethod
    async def get_cart(self) -> ShoppingCart:
        pass

    @abstractmethod
    async def place_order(self) -> ShoppingCart:
        pass


class CartService(ICartService):
    def __init__(
        self,
        db: Db = Depends(get_db),
        product_service: ProductService = Depends(),
        cart_id=Depends(get_cart_id),
    ):
        self.product_service = product_service
        self.cart_repo = CartRepository(db)
        self.cart_id = cart_id

    async def get_cart(self) -> ShoppingCart:
        cart_orm = await self.get_cart_orm()
        shopping_cart = ShoppingCart()
        for product in cart_orm.cart_products:
            shopping_cart.add_product(CartProduct.from_orm(product))
        shopping_cart_calculator = ShoppingCartCalculator(shopping_cart=shopping_cart)
        try:
            total_amount = shopping_cart_calculator.calculate_cart()
        except ShoppingCartError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        return ShoppingCart(
            total_amount=total_amount, cart_products=cart_orm.cart_products
        )

    async def add_product(self, product_id: int, amount: int) -> TotalAmount:
        await self.product_service.get_product_by_id(product_id)  # todo: ???
        cart_orm = await self.get_cart_orm()
        await self.cart_repo.add_product(cart_orm, product_id, amount)
        shopping_cart = ShoppingCart()
        for product in cart_orm.cart_products:
            shopping_cart.add_product(CartProduct.from_orm(product))
        shopping_cart_calculator = ShoppingCartCalculator(shopping_cart=shopping_cart)
        try:
            total_amount = shopping_cart_calculator.calculate_cart()
        except ShoppingCartError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        return TotalAmount(total_amount=total_amount)

    async def place_order(self) -> ShoppingCart:
        cart_orm = await self.get_cart_orm()
        shopping_cart = ShoppingCart()
        for product in cart_orm.cart_products:
            shopping_cart.add_product(CartProduct.from_orm(product))
        shopping_cart_calculator = ShoppingCartCalculator(shopping_cart=shopping_cart)
        try:
            total_amount = shopping_cart_calculator.calculate_cart()
        except ShoppingCartError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        await self.cart_repo.delete_order(cart_orm)
        return ShoppingCart(
            total_amount=total_amount, cart_products=cart_orm.cart_products
        )

    async def get_cart_orm(self) -> orm.cart.Cart:
        cart_orm = await self.cart_repo.get_cart(self.cart_id)
        if not cart_orm:
            cart_orm = await self.cart_repo.create_cart(self.cart_id)
        return cart_orm
