from .base import BaseRepository
from src.models.core.cart import ShoppingCart, CartProduct
from src.models.core.products import Product

cart_db = {
    "default": ShoppingCart(
        cart_products=[
            CartProduct(amount=1, product=Product(id=1, name='melon', price=2))
        ]
    )
}


class CartRepository(BaseRepository):
    async def get_cart(self, cart_id: str) -> ShoppingCart | None:
        if cart_id in cart_db:
            return cart_db[cart_id]
        else:
            return None

    async def create_cart(self, cart_id: str) -> ShoppingCart:
        empty_cart = ShoppingCart(cart_products=[])
        cart_db[cart_id] = empty_cart
        return empty_cart

    async def add_product(self, cart: ShoppingCart, cart_product: CartProduct):
        cart.add_product(cart_product)
