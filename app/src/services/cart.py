from abc import abstractmethod, ABC

from fastapi import HTTPException
from fastapi import Depends

from src.database import Db
from src.deps.common import get_db
from src.deps.cart import get_session_id
from src.repositories.cart import CartRepository
from src.models.core.cart import CartProduct, ShoppingCart, TotalAmount
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
        session_id=Depends(get_session_id),
    ):
        self.product_service = product_service
        self.cart_repo = CartRepository(db)
        self.session_id = session_id

    async def get_cart(self) -> ShoppingCart:
        cart = await self.get_cart_orm()
        return await self.create_shopping_cart(cart)

    async def add_product(self, product_id: int, amount: int) -> TotalAmount:
        await self.product_service.validate_if_product_exists(product_id)
        cart = await self.get_cart_orm()
        await self.cart_repo.add_product(cart, product_id, amount)
        shopping_cart = await self.create_shopping_cart(cart)
        return TotalAmount(total_amount=shopping_cart.total_amount)

    async def place_order(self) -> ShoppingCart:
        cart = await self.get_cart_orm()
        shopping_cart = await self.create_shopping_cart(cart)
        await self.cart_repo.delete_cart(cart)
        return shopping_cart

    async def get_cart_orm(self) -> orm.cart.Cart:
        cart = await self.cart_repo.get_cart(self.session_id)
        if not cart:
            cart = await self.cart_repo.create_cart(self.session_id)
        return cart

    async def create_shopping_cart(self, cart_orm: orm.cart.Cart) -> ShoppingCart:
        shopping_cart = ShoppingCart()
        shopping_cart.add_products(
            [CartProduct.from_orm(product) for product in cart_orm.cart_products]
        )
        shopping_cart_calculator = ShoppingCartCalculator(shopping_cart=shopping_cart)
        try:
            shopping_cart_calculator.calculate_cart()
        except ShoppingCartError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        return shopping_cart
