from sqlalchemy import select, update

from .base import BaseRepository
from src.models.core.cart import ShoppingCart, CartProduct
from src.models.core.products import Product
from src.models.orm.cart import Carts as CartsORM, CartProducts as CartProductsOrm
from sqlalchemy.dialects.postgresql import insert

cart_db = {
    "default": ShoppingCart(
        cart_products=[
            CartProduct(amount=1, product=Product(id=1, name="melon", price=2))
        ]
    )
}


class CartRepository(BaseRepository):
    async def get_cart(self, cart_id: str) -> CartsORM | None:
        carts_orm = await self.db.scalar(
            select(CartsORM)
            .filter(CartsORM.cart_id == cart_id)
            .filter(CartsORM.is_placed == False)
        )
        if not carts_orm:
            return None
        else:
            return carts_orm

    async def create_cart(self, cart_id: str) -> CartsORM:
        empty_cart = CartsORM(cart_id=cart_id, cart_products=[])
        self.db.add(
            empty_cart
        )
        await self.db.flush()
        return empty_cart

    async def add_product(self, cart: CartsORM, product_id: int, amount: int):
        stmt = insert(CartProductsOrm).values(product_id=product_id, amount=amount, carts_id=cart.id)
        excluded = dict(stmt.excluded)
        excluded.pop("carts_id")
        excluded.pop("product_id")
        stmt = stmt.on_conflict_do_update(
            index_elements=[CartProductsOrm.carts_id, CartProductsOrm.product_id],
            set_=dict(excluded)
        )
        await self.db.execute(stmt)
        await self.db.refresh(cart)

    async def delete_order(self, cart_orm: CartsORM):
        cart_orm.is_placed = True
