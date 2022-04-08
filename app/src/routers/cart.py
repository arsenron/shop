from fastapi import APIRouter, Depends
from src.services.cart import ICartService, CartService

router = APIRouter(
    prefix="/cart"
)


@router.post("/add/{product_id}")
async def add_to_cart(product_id: int, amount: int = 1, svc: CartService = Depends(CartService)):
    return await svc.add_product(product_id, amount)
