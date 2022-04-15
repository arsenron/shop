from abc import abstractmethod, ABC

from fastapi import HTTPException
from fastapi import Depends

from src.database import Db
from src.deps.common import get_db
from src.deps.cart import get_session_id
from src.repositories.cart import CartRepository
from src.models.core.cart import CartProduct, ShoppingCart, TotalAmount
from src.models.orm.cart import CartOrm
from .calculations.cart_calculator import ShoppingCartCalculator
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
        cart_orm = await self.get_cart_orm()
        return await self.create_shopping_cart(cart_orm)

    async def add_product(self, product_id: int, amount: int) -> TotalAmount:
        await self.product_service.validate_if_product_exists(product_id)
        cart_orm = await self.get_cart_orm()
        await self.cart_repo.add_product(cart_orm, product_id, amount)
        shopping_cart = await self.create_shopping_cart(cart_orm)
        return TotalAmount(total_amount=shopping_cart.total_amount)

    async def place_order(self) -> ShoppingCart:
        cart_orm = await self.get_cart_orm()
        shopping_cart = await self.create_shopping_cart(cart_orm)
        await self.cart_repo.place_cart(cart_orm)
        return shopping_cart

    async def get_cart_orm(self) -> CartOrm:
        cart_orm = await self.cart_repo.get_cart(self.session_id)
        if not cart_orm:
            cart_orm = await self.cart_repo.create_cart(self.session_id)
        return cart_orm

    async def create_shopping_cart(self, cart_orm: CartOrm) -> ShoppingCart:
        shopping_cart = ShoppingCart(
            cart_products=[CartProduct.from_orm(product) for product in cart_orm.cart_products]
        )
        shopping_cart_calculator = ShoppingCartCalculator(shopping_cart=shopping_cart)
        try:
            shopping_cart_calculator.apply_calculation_rules()
        except ShoppingCartError as exc:
            await self.cart_repo.rollback()
            raise HTTPException(status_code=400, detail=str(exc))
        return shopping_cart
