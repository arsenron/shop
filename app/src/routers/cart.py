from fastapi import APIRouter, Depends, Request
from src.services.cart import ICartService, CartService
from src.models.schemas.cart import ShoppingCart

router = APIRouter(prefix="/cart")


@router.post("/add/{product_id}")
async def add_to_cart(
    product_id: int, amount: int = 1, svc: CartService = Depends(CartService)
):
    return await svc.add_product(product_id, amount)


@router.post("/place", response_model=ShoppingCart)
async def place_order(svc: CartService = Depends(CartService)):
    cart = await svc.place_order()
    return cart
