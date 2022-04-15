from sqlalchemy import select

from .base import BaseRepository
from sqlalchemy.dialects.postgresql import insert
from src.models.orm.cart import CartOrm, CartProductsOrm


class CartRepository(BaseRepository):
    async def get_cart(self, session_id: str) -> CartOrm | None:
        return await self.db.scalar(
            select(CartOrm).filter(CartOrm.session_id == session_id).filter(CartOrm.is_placed == False)
        )

    async def create_cart(self, session_id: str) -> CartOrm:
        empty_cart = CartOrm(session_id=session_id, cart_products=[])
        self.db.add(empty_cart)
        await self.db.flush()
        return empty_cart

    async def add_product(self, cart: CartOrm, product_id: int, amount: int):
        stmt = insert(CartProductsOrm).values(product_id=product_id, amount=amount, carts_id=cart.id)
        excluded = dict(stmt.excluded)
        excluded.pop("carts_id")
        excluded.pop("product_id")
        stmt = stmt.on_conflict_do_update(
            index_elements=[CartProductsOrm.carts_id, CartProductsOrm.product_id],
            set_=dict(excluded),
        )
        await self.db.execute(stmt)
        await self.db.refresh(cart)

    async def place_cart(self, cart: CartOrm):
        cart.is_placed = True
