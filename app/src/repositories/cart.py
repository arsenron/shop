from sqlalchemy import select

from .base import BaseRepository
from sqlalchemy.dialects.postgresql import insert
from src.models.orm.cart import Cart, CartProducts


class CartRepository(BaseRepository):
    async def get_cart(self, cart_id: str) -> Cart | None:
        cart = await self.db.scalar(
            select(Cart)
            .filter(Cart.cart_id == cart_id)
            .filter(Cart.is_placed == False)
        )
        if not cart:
            return None
        else:
            return cart

    async def create_cart(self, cart_id: str) -> Cart:
        empty_cart = Cart(cart_id=cart_id, cart_products=[])
        self.db.add(
            empty_cart
        )
        await self.db.flush()
        return empty_cart

    async def add_product(self, cart: Cart, product_id: int, amount: int):
        stmt = insert(CartProducts).values(product_id=product_id, amount=amount, carts_id=cart.id)
        excluded = dict(stmt.excluded)
        excluded.pop("carts_id")
        excluded.pop("product_id")
        stmt = stmt.on_conflict_do_update(
            index_elements=[CartProducts.carts_id, CartProducts.product_id],
            set_=dict(excluded)
        )
        await self.db.execute(stmt)
        await self.db.refresh(cart)

    async def delete_order(self, cart: Cart):
        cart.is_placed = True
