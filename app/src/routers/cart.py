from fastapi import APIRouter, Depends
from src.services.cart import ICartService, CartService
from src.models.core.cart import ShoppingCartSchema

router = APIRouter(prefix="/cart")


@router.post("/add/{product_id}")
async def add_to_cart(
    product_id: int, amount: int = 1, svc: CartService = Depends(CartService)
):
    return await svc.add_product(product_id, amount)


@router.post("/place", response_model=ShoppingCartSchema)
async def place_order(svc: CartService = Depends(CartService)):
    cart = await svc.place_order()
    return cart
